"""
测试 AK (Access Key) 认证功能的脚本

用法:
    python test_ak_auth.py --access-key "你的AK" --secret-key "你的SK"
    或者
    python test_ak_auth.py --api-url "http://localhost:8000"
"""

import requests
import argparse
import json
import sys


def test_ak_auth(base_url, access_key, secret_key):
    """测试 AK 认证功能"""

    headers = {
        "Authorization": f"AK-SK {access_key}:{secret_key}",
        "Content-Type": "application/json"
    }

    print(f"测试 AK 认证...")
    print(f"API 地址: {base_url}")
    print(f"Access Key: {access_key}")
    print(f"Secret Key: {secret_key[:10]}..." if len(secret_key) > 10 else f"Secret Key: {secret_key}")
    print("-" * 60)

    # 测试 1: 获取用户信息
    print("\n1. 测试获取用户信息 (GET /api/v1/user)")
    try:
        response = requests.get(
            f"{base_url}/api/v1/user",
            headers=headers
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   成功: {data.get('message', 'OK')}")
            print(f"   用户名: {data.get('data', {}).get('username', 'N/A')}")
        else:
            print(f"   失败: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")

    # 测试 2: 获取公众号列表
    print("\n2. 测试获取公众号列表 (GET /api/v1/mps)")
    try:
        response = requests.get(
            f"{base_url}/api/v1/mps",
            headers=headers
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   成功: {data.get('message', 'OK')}")
            total = data.get('data', {}).get('total', 0)
            print(f"   公众号总数: {total}")
        else:
            print(f"   失败: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")

    # 测试 3: 获取文章列表
    print("\n3. 测试获取文章列表 (GET /api/v1/articles)")
    try:
        response = requests.get(
            f"{base_url}/api/v1/articles",
            headers=headers
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   成功: {data.get('message', 'OK')}")
            total = data.get('data', {}).get('total', 0)
            print(f"   文章总数: {total}")
        else:
            print(f"   失败: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")

    # 测试 4: 获取系统信息
    print("\n4. 测试获取系统信息 (GET /api/v1/sys/info)")
    try:
        response = requests.get(
            f"{base_url}/api/v1/sys/info",
            headers=headers
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   成功: {data.get('message', 'OK')}")
            sys_info = data.get('data', {})
            print(f"   API 版本: {sys_info.get('api_version', 'N/A')}")
            print(f"   核心版本: {sys_info.get('core_version', 'N/A')}")
        else:
            print(f"   失败: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")

    # 测试 5: 获取 Access Keys 列表 (需要先登录获取 JWT token)
    print("\n5. 测试获取 Access Keys 列表 (GET /api/v1/auth/ak/list)")
    print("   注意: 此接口需要 JWT Token，AK 无法访问")
    try:
        response = requests.get(
            f"{base_url}/api/v1/auth/ak/list",
            headers=headers
        )
        print(f"   状态码: {response.status_code}")
        print(f"   说明: AK 管理接口应拒绝 AK 访问，使用 JWT 认证")
        if response.status_code == 401:
            print(f"   正确: AK 无法访问 AK 管理接口 (符合安全要求)")
        else:
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")

    print("\n" + "=" * 60)
    print("测试完成!")


def test_jwt_auth(base_url, username, password):
    """测试 JWT 认证并创建 AK"""

    print("\n" + "=" * 60)
    print("测试 JWT 认证并创建 Access Key")
    print("=" * 60)

    # 1. 登录获取 JWT token
    print("\n1. 登录获取 JWT Token")
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            data={
                "username": username,
                "password": password
            }
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('access_token')
            print(f"   登录成功")
            print(f"   Token: {token[:20]}..." if len(token) > 20 else f"   Token: {token}")
        else:
            print(f"   登录失败: {response.text}")
            return None, None
    except Exception as e:
        print(f"   错误: {str(e)}")
        return None, None

    if not token:
        print("   无法获取 Token")
        return None, None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 2. 创建 Access Key
    print("\n2. 创建新的 Access Key")
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/ak/create",
            headers=headers,
            json={
                "name": "测试 AK",
                "description": "用于测试 AK 认证功能",
                "permissions": [],
                "expires_in_days": None
            }
        )
        if response.status_code == 200:
            data = response.json()
            ak_data = data.get('data', {})
            access_key = ak_data.get('key')
            secret_key = ak_data.get('secret')
            print(f"   创建成功")
            print(f"   Access Key: {access_key}")
            print(f"   Secret Key: {secret_key}")
            print(f"\n   重要: Secret Key 只会显示一次，请妥善保存！")
            return access_key, secret_key
        else:
            print(f"   创建失败: {response.text}")
            return None, None
    except Exception as e:
        print(f"   错误: {str(e)}")
        return None, None


def main():
    parser = argparse.ArgumentParser(description='测试 AK 认证功能')
    parser.add_argument('--api-url', default='http://localhost:8000',
                        help='API 服务器地址 (默认: http://localhost:8000)')
    parser.add_argument('--access-key', '-k',
                        help='Access Key (如果不提供，将尝试登录创建)')
    parser.add_argument('--secret-key', '-s',
                        help='Secret Key (如果不提供，将尝试登录创建)')
    parser.add_argument('--username', '-u',
                        help='用户名 (用于创建 AK)')
    parser.add_argument('--password', '-p',
                        help='密码 (用于创建 AK)')

    args = parser.parse_args()

    base_url = args.api_url.rstrip('/')

    # 如果提供了 AK/SK，直接测试
    if args.access_key and args.secret_key:
        test_ak_auth(base_url, args.access_key, args.secret_key)
    # 否则尝试登录创建 AK
    elif args.username and args.password:
        access_key, secret_key = test_jwt_auth(base_url, args.username, args.password)
        if access_key and secret_key:
            print("\n使用新创建的 AK 进行测试...")
            test_ak_auth(base_url, access_key, secret_key)
    else:
        print("请提供以下参数之一:")
        print("  1. 使用现有的 AK:")
        print("     python test_ak_auth.py --access-key AK_VALUE --secret-key SK_VALUE")
        print("  2. 登录创建新的 AK:")
        print("     python test_ak_auth.py --username USERNAME --password PASSWORD")
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
