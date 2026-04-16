"download_detour": "select",
                    "update_interval": "1d"
                }
            ],
            "final": "select",
            "auto_detect_interface": True
        },
        "experimental": {
            "clash_api": {
                "external_controller": "127.0.0.1:9090",
                "secret": "",
                "external_ui": "metacubexd",
                "external_ui_download_url": "https://github.com/MetaCubeX/metacubexd/archive/gh-pages.zip",
                "external_ui_download_detour": "select"
            },
            "cache_file": {
                "enabled": True,
                "path": "cache.db",
                "store_fakeip": False
            }
        }
    }
    
    return config

def main():
    print("开始获取订阅...")
    content = fetch_subscribe(SUBSCRIBE_URL)
    
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    
    outbounds = []
    tags = []
    
    for line in lines:
        try:
            if line.startswith("vless://"):
                ob, tag = parse_vless(line)
                outbounds.append(ob)
                tags.append(tag)
                print(f"✓ vless: {tag}")
            elif line.startswith("vmess://"):
                ob, tag = parse_vmess(line)
                outbounds.append(ob)
                tags.append(tag)
                print(f"✓ vmess: {tag}")
            elif line.startswith("trojan://"):
                ob, tag = parse_trojan(line)
                outbounds.append(ob)
                tags.append(tag)
                print(f"✓ trojan: {tag}")
            elif line.startswith("ss://"):
                ob, tag = parse_ss(line)
                outbounds.append(ob)
                tags.append(tag)
                print(f"✓ ss: {tag}")
            else:
                pass
        except Exception as e:
            print(f"✗ 解析失败: {line[:50]} | 错误: {e}")
    
    if not outbounds:
        print("没有解析到任何节点，请检查订阅链接")
        return
    
    print(f"\n共解析 {len(outbounds)} 个节点")
    
    config = build_config(outbounds, tags)
    
    os.makedirs("output", exist_ok=True)
    with open("output/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✓ 配置已生成：output/config.json")

if name == "main":
    main()
