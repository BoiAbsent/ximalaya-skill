#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喜马拉雅开放平台API调用客户端

支持OAuth 2.0鉴权，提供统一的API调用接口
凭证在执行时通过参数传递，由智能体引导用户完成OAuth授权流程
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

import requests


class XimalayaAPIClient:
    """喜马拉雅API客户端"""
    
    def __init__(self, access_token: str):
        """
        初始化客户端
        
        Args:
            access_token: OAuth访问令牌
        """
        if not access_token:
            raise ValueError("access_token不能为空")
        
        self.access_token = access_token
        self.base_url = "https://api.ximalaya.com"
    
    def _build_url(self, endpoint: str) -> str:
        """构建完整的API URL"""
        # 移除endpoint开头的斜杠
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _build_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        """构建请求头"""
        headers = {
            "Content-Type": content_type,
            "Authorization": f"Bearer {self.access_token}"
        }
        return headers
    
    def _parse_params(self, params_str: Optional[str]) -> Dict[str, Any]:
        """解析参数字符串为字典"""
        if not params_str:
            return {}
        
        try:
            # 尝试解析JSON格式
            return json.loads(params_str)
        except json.JSONDecodeError:
            # 解析为key=value格式
            params = {}
            for item in params_str.split('&'):
                if '=' in item:
                    key, value = item.split('=', 1)
                    params[key] = value
            return params
    
    def _parse_json_body(self, body_str: Optional[str]) -> Optional[Dict[str, Any]]:
        """解析JSON请求体"""
        if not body_str:
            return None
        try:
            return json.loads(body_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON请求体格式错误: {str(e)}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理API响应"""
        # 检查HTTP状态码
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        # 解析JSON响应
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"响应解析失败: {response.text}")
        
        # 检查业务错误码
        if isinstance(data, dict):
            if data.get("ret") != 0 or data.get("errcode", 0) != 0:
                error_msg = data.get("msg", data.get("errmsg", "未知错误"))
                error_code = data.get("ret", data.get("errcode", "unknown"))
                raise Exception(f"API错误[{error_code}]: {error_msg}")
        
        return data
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        通用API请求方法
        
        Args:
            method: HTTP方法 (GET/POST/PUT/DELETE)
            endpoint: API端点路径
            params: URL查询参数
            body: 请求体数据（POST/PUT使用）
            timeout: 超时时间（秒）
        
        Returns:
            API响应数据
        
        Raises:
            Exception: 请求失败或API返回错误时抛出
        """
        url = self._build_url(endpoint)
        headers = self._build_headers()
        
        method_upper = method.upper()
        
        try:
            if method_upper == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method_upper == "POST":
                response = requests.post(url, headers=headers, params=params, json=body, timeout=timeout)
            elif method_upper == "PUT":
                response = requests.put(url, headers=headers, params=params, json=body, timeout=timeout)
            elif method_upper == "DELETE":
                response = requests.delete(url, headers=headers, params=params, timeout=timeout)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            return self._handle_response(response)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="喜马拉雅开放平台API调用客户端")
    parser.add_argument("--access-token", required=True, help="OAuth访问令牌")
    parser.add_argument("--method", required=True, help="HTTP方法: GET/POST/PUT/DELETE")
    parser.add_argument("--endpoint", required=True, help="API端点路径，例如: /v1/albums")
    parser.add_argument("--params", help="URL查询参数，格式: key1=value1&key2=value2 或JSON字符串")
    parser.add_argument("--body", help="请求体数据（POST/PUT），格式: JSON字符串")
    parser.add_argument("--timeout", type=int, default=30, help="超时时间（秒），默认30")
    
    args = parser.parse_args()
    
    try:
        # 创建客户端
        client = XimalayaAPIClient(access_token=args.access_token)
        
        # 解析参数
        params = client._parse_params(args.params) if args.params else None
        body = client._parse_json_body(args.body) if args.body else None
        
        # 发起请求
        result = client.request(
            method=args.method,
            endpoint=args.endpoint,
            params=params,
            body=body,
            timeout=args.timeout
        )
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
