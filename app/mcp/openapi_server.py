#!/usr/bin/env python3
"""
MCP Server для генерации кода на основе OpenAPI спецификации
Генерирует модели SQLAlchemy, маршруты Flask и валидацию
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
import yaml

# Добавляем поддержку MCP
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import Resource, Tool, TextContent
except ImportError:
    print("Установите mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

class OpenAPIMCPServer:
    def __init__(self):
        self.server = Server("openapi-codegen-server")
        self.spec_path = os.getenv('OPENAPI_SPEC_PATH', 'api/openapi.yaml')
        self.spec_data = None
        
        # Загружаем спецификацию при инициализации
        self._load_spec()
        
        # Регистрируем инструменты
        self._register_tools()
    
    def _load_spec(self):
        """Загружает OpenAPI спецификацию"""
        try:
            if os.path.exists(self.spec_path):
                with open(self.spec_path, 'r', encoding='utf-8') as f:
                    if self.spec_path.endswith('.yaml') or self.spec_path.endswith('.yml'):
                        self.spec_data = yaml.safe_load(f)
                    else:
                        self.spec_data = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки спецификации: {e}", file=sys.stderr)
    
    def _register_tools(self):
        """Регистрация всех инструментов MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return [
                Tool(
                    name="generate_model",
                    description="Генерирует модель SQLAlchemy на основе OpenAPI схемы",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "schema_name": {
                                "type": "string",
                                "description": "Имя схемы из OpenAPI для генерации модели"
                            },
                            "table_name": {
                                "type": "string",
                                "description": "Имя таблицы (опционально, по умолчанию из schema_name)"
                            }
                        },
                        "required": ["schema_name"]
                    }
                ),
                Tool(
                    name="generate_route",
                    description="Генерирует Flask маршрут на основе OpenAPI пути",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Путь из OpenAPI спецификации"
                            },
                            "method": {
                                "type": "string",
                                "description": "HTTP метод (GET, POST, PUT, DELETE)"
                            }
                        },
                        "required": ["path", "method"]
                    }
                ),
                Tool(
                    name="validate_spec",
                    description="Валидирует OpenAPI спецификацию",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="list_schemas",
                    description="Получает список всех схем из OpenAPI спецификации",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            try:
                if name == "generate_model":
                    return await self._handle_generate_model(arguments)
                elif name == "generate_route":
                    return await self._handle_generate_route(arguments)
                elif name == "validate_spec":
                    return await self._handle_validate_spec(arguments)
                elif name == "list_schemas":
                    return await self._handle_list_schemas(arguments)
                else:
                    raise ValueError(f"Неизвестный инструмент: {name}")
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Ошибка выполнения {name}: {str(e)}"
                )]
    
    async def _handle_generate_model(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Генерирует модель SQLAlchemy"""
        if not self.spec_data:
            return [TextContent(
                type="text",
                text="Ошибка: OpenAPI спецификация не загружена"
            )]
        
        schema_name = arguments.get("schema_name")
        table_name = arguments.get("table_name", schema_name.lower())
        
        schemas = self.spec_data.get("components", {}).get("schemas", {})
        if schema_name not in schemas:
            return [TextContent(
                type="text",
                text=f"Ошибка: Схема '{schema_name}' не найдена в спецификации"
            )]
        
        schema = schemas[schema_name]
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        # Генерируем код модели
        model_code = self._generate_sqlalchemy_model(schema_name, table_name, properties, required)
        
        return [TextContent(
            type="text",
            text=model_code
        )]
    
    def _generate_sqlalchemy_model(self, class_name: str, table_name: str, properties: Dict, required: List[str]) -> str:
        """Генерирует код модели SQLAlchemy"""
        imports = [
            "from flask_sqlalchemy import SQLAlchemy",
            "from datetime import datetime",
            ""
        ]
        
        class_def = [
            f"class {class_name}(db.Model):",
            f"    __tablename__ = '{table_name}'",
            ""
        ]
        
        # Генерируем поля
        for prop_name, prop_def in properties.items():
            field_type = self._map_openapi_type_to_sqlalchemy(prop_def)
            nullable = prop_name not in required
            
            if prop_name == 'id':
                class_def.append(f"    {prop_name} = db.Column({field_type}, primary_key=True)")
            else:
                class_def.append(f"    {prop_name} = db.Column({field_type}, nullable={nullable})")
        
        # Добавляем метод __repr__
        class_def.extend([
            "",
            f"    def __repr__(self):",
            f"        return f'<{class_name} {{self.id}}>'"
        ])
        
        return "\n".join(imports + class_def)
    
    def _map_openapi_type_to_sqlalchemy(self, prop_def: Dict) -> str:
        """Маппинг типов OpenAPI в типы SQLAlchemy"""
        openapi_type = prop_def.get("type", "string")
        format_type = prop_def.get("format")
        
        type_mapping = {
            "string": "db.String(255)",
            "integer": "db.Integer",
            "number": "db.Float",
            "boolean": "db.Boolean",
            "array": "db.Text",  # Можно использовать JSON
            "object": "db.JSON"
        }
        
        if openapi_type == "string":
            if format_type == "date-time":
                return "db.DateTime"
            elif format_type == "date":
                return "db.Date"
            elif format_type == "email":
                return "db.String(255)"
            elif "maxLength" in prop_def:
                return f"db.String({prop_def['maxLength']})"
        
        return type_mapping.get(openapi_type, "db.String(255)")
    
    async def _handle_generate_route(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Генерирует Flask маршрут"""
        if not self.spec_data:
            return [TextContent(
                type="text",
                text="Ошибка: OpenAPI спецификация не загружена"
            )]
        
        path = arguments.get("path")
        method = arguments.get("method", "GET").upper()
        
        paths = self.spec_data.get("paths", {})
        if path not in paths:
            return [TextContent(
                type="text",
                text=f"Ошибка: Путь '{path}' не найден в спецификации"
            )]
        
        path_info = paths[path]
        method_info = path_info.get(method.lower(), {})
        
        if not method_info:
            return [TextContent(
                type="text",
                text=f"Ошибка: Метод '{method}' не найден для пути '{path}'"
            )]
        
        # Генерируем код маршрута
        route_code = self._generate_flask_route(path, method, method_info)
        
        return [TextContent(
            type="text",
            text=route_code
        )]
    
    def _generate_flask_route(self, path: str, method: str, method_info: Dict) -> str:
        """Генерирует код Flask маршрута"""
        operation_id = method_info.get("operationId", f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '')}")
        summary = method_info.get("summary", "")
        
        # Преобразуем путь OpenAPI в Flask формат
        flask_path = path.replace("{", "<").replace("}", ">")
        
        route_code = [
            f"@app.route('{flask_path}', methods=['{method}'])",
            f"def {operation_id}():",
            f'    """',
            f'    {summary}',
            f'    """'
        ]
        
        # Добавляем базовую логику в зависимости от метода
        if method == "GET":
            route_code.extend([
                "    try:",
                "        # TODO: Реализовать логику получения данных",
                "        return jsonify({'message': 'Success'}), 200",
                "    except Exception as e:",
                "        return jsonify({'error': str(e)}), 500"
            ])
        elif method == "POST":
            route_code.extend([
                "    try:",
                "        data = request.get_json()",
                "        # TODO: Валидация и сохранение данных",
                "        return jsonify({'message': 'Created'}), 201",
                "    except Exception as e:",
                "        return jsonify({'error': str(e)}), 400"
            ])
        elif method == "PUT":
            route_code.extend([
                "    try:",
                "        data = request.get_json()",
                "        # TODO: Обновление данных",
                "        return jsonify({'message': 'Updated'}), 200",
                "    except Exception as e:",
                "        return jsonify({'error': str(e)}), 400"
            ])
        elif method == "DELETE":
            route_code.extend([
                "    try:",
                "        # TODO: Удаление данных",
                "        return jsonify({'message': 'Deleted'}), 200",
                "    except Exception as e:",
                "        return jsonify({'error': str(e)}), 400"
            ])
        
        return "\n".join(route_code)
    
    async def _handle_validate_spec(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Валидирует OpenAPI спецификацию"""
        if not self.spec_data:
            return [TextContent(
                type="text",
                text="Ошибка: OpenAPI спецификация не загружена"
            )]
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": {
                "version": self.spec_data.get("openapi", "не указана"),
                "title": self.spec_data.get("info", {}).get("title", "не указан"),
                "paths_count": len(self.spec_data.get("paths", {})),
                "schemas_count": len(self.spec_data.get("components", {}).get("schemas", {}))
            }
        }
        
        # Базовая валидация
        if "openapi" not in self.spec_data:
            validation_result["errors"].append("Отсутствует поле 'openapi'")
            validation_result["valid"] = False
        
        if "info" not in self.spec_data:
            validation_result["errors"].append("Отсутствует поле 'info'")
            validation_result["valid"] = False
        
        if "paths" not in self.spec_data:
            validation_result["warnings"].append("Отсутствует поле 'paths'")
        
        return [TextContent(
            type="text",
            text=json.dumps(validation_result, indent=2, ensure_ascii=False)
        )]
    
    async def _handle_list_schemas(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Получает список всех схем"""
        if not self.spec_data:
            return [TextContent(
                type="text",
                text="Ошибка: OpenAPI спецификация не загружена"
            )]
        
        schemas = self.spec_data.get("components", {}).get("schemas", {})
        schema_list = []
        
        for schema_name, schema_def in schemas.items():
            schema_info = {
                "name": schema_name,
                "type": schema_def.get("type", "object"),
                "properties": list(schema_def.get("properties", {}).keys()),
                "required": schema_def.get("required", [])
            }
            schema_list.append(schema_info)
        
        return [TextContent(
            type="text",
            text=json.dumps(schema_list, indent=2, ensure_ascii=False)
        )]

async def main():
    """Запуск MCP сервера"""
    openapi_server = OpenAPIMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await openapi_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="openapi-codegen-server",
                server_version="1.0.0",
                capabilities=openapi_server.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())