#!/usr/bin/env python3
"""
MCP Server для работы с PostgreSQL (только чтение)
Предоставляет инструменты для выполнения SQL-запросов и получения схемы БД
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# Добавляем поддержку MCP
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import Resource, Tool, TextContent
except ImportError:
    print("Установите mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

class PostgreSQLMCPServer:
    def __init__(self):
        self.server = Server("postgresql-mcp-server")
        self.connection_params = {
            'dbname': os.getenv('DB_NAME', 'flask_app'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        # Регистрируем инструменты
        self._register_tools()
        
    def _register_tools(self):
        """Регистрация всех инструментов MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return [
                Tool(
                    name="pg_query",
                    description="Выполняет SQL-запросы только для чтения к PostgreSQL",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL-запрос для выполнения (только SELECT)"
                            },
                            "params": {
                                "type": "object",
                                "description": "Параметры для SQL-запроса",
                                "additionalProperties": True
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_schema",
                    description="Получает схему базы данных",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {
                                "type": "string",
                                "description": "Имя таблицы (опционально)"
                            }
                        }
                    }
                ),
                Tool(
                    name="list_tables",
                    description="Получает список всех таблиц в базе данных",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            try:
                if name == "pg_query":
                    return await self._handle_pg_query(arguments)
                elif name == "get_schema":
                    return await self._handle_get_schema(arguments)
                elif name == "list_tables":
                    return await self._handle_list_tables(arguments)
                else:
                    raise ValueError(f"Неизвестный инструмент: {name}")
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Ошибка выполнения {name}: {str(e)}"
                )]
    
    async def _handle_pg_query(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Выполняет SQL-запрос только для чтения"""
        query = arguments.get("query", "")
        params = arguments.get("params", {})
        
        # Проверяем, что это запрос только для чтения
        query_upper = query.strip().upper()
        if not query_upper.startswith(('SELECT', 'WITH', 'EXPLAIN')):
            return [TextContent(
                type="text",
                text="Ошибка: Разрешены только запросы SELECT, WITH и EXPLAIN"
            )]
        
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    
                    if cur.description:
                        columns = [desc.name for desc in cur.description]
                        rows = cur.fetchall()
                        
                        # Форматируем результат
                        result = {
                            "columns": columns,
                            "rows": [dict(row) for row in rows],
                            "row_count": len(rows)
                        }
                    else:
                        result = {"status": "success", "message": "Запрос выполнен успешно"}
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2, ensure_ascii=False, default=str)
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Ошибка выполнения запроса: {str(e)}"
            )]
    
    async def _handle_get_schema(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Получает схему базы данных"""
        table_name = arguments.get("table_name")
        
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    if table_name:
                        # Схема конкретной таблицы
                        query = """
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable,
                            column_default,
                            character_maximum_length
                        FROM information_schema.columns 
                        WHERE table_name = %s 
                        ORDER BY ordinal_position
                        """
                        cur.execute(query, (table_name,))
                    else:
                        # Общая схема всех таблиц
                        query = """
                        SELECT 
                            table_name,
                            column_name,
                            data_type,
                            is_nullable,
                            column_default
                        FROM information_schema.columns 
                        WHERE table_schema = 'public'
                        ORDER BY table_name, ordinal_position
                        """
                        cur.execute(query)
                    
                    rows = cur.fetchall()
                    result = [dict(row) for row in rows]
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2, ensure_ascii=False, default=str)
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Ошибка получения схемы: {str(e)}"
            )]
    
    async def _handle_list_tables(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Получает список всех таблиц"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    query = """
                    SELECT 
                        table_name,
                        table_type
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                    """
                    cur.execute(query)
                    
                    rows = cur.fetchall()
                    result = [dict(row) for row in rows]
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2, ensure_ascii=False)
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Ошибка получения списка таблиц: {str(e)}"
            )]

async def main():
    """Запуск MCP сервера"""
    pg_server = PostgreSQLMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await pg_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="postgresql-mcp-server",
                server_version="1.0.0",
                capabilities=pg_server.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())