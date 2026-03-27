import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
processes = []


def start_process(name, cmd):
    print(f"🚀 啟動 {name}...")
    try:
        process = subprocess.Popen(
            cmd,
            cwd=BASE_DIR,
        )
        processes.append(
            {
                "name": name,
                "process": process,
                "stopped_logged": False,
            }
        )
        return process
    except Exception as e:
        print(f"❌ 啟動 {name} 失敗：{e}")
        return None


def stop_all():
    print("\n🛑 正在停止所有服務...")

    # 先嘗試正常結束
    for item in processes:
        name = item["name"]
        process = item["process"]

        if process.poll() is None:
            try:
                print(f"⛔ 停止 {name}")
                process.terminate()
            except Exception as e:
                print(f"⚠️ 停止 {name} 時發生錯誤：{e}")

    # 等待結束，必要時強制 kill
    for item in processes:
        name = item["name"]
        process = item["process"]

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                print(f"⚠️ {name} 未正常結束，改用強制停止")
                process.kill()
            except Exception as e:
                print(f"⚠️ 強制停止 {name} 失敗：{e}")
        except Exception as e:
            print(f"⚠️ 等待 {name} 結束時發生錯誤：{e}")


def monitor():
    while True:
        for item in processes:
            name = item["name"]
            process = item["process"]

            if process.poll() is not None and not item["stopped_logged"]:
                print(f"⚠️ {name} 已停止（不自動重啟）")
                item["stopped_logged"] = True

        time.sleep(5)


def main():
    try:
        # Gunicorn
        start_process(
            "Gunicorn",
            [
                "gunicorn",
                "-w", "2",
                "-b", "0.0.0.0:5000",
                "app:app",
            ],
        )

        # Market Worker
        start_process(
            "Market Worker",
            [sys.executable, "workers/market_worker.py"],
        )

        # Cloudflare Tunnel
        # 若你的 tunnel 名稱不是 ai-stock，改成你自己的名稱
        start_process(
            "Cloudflare Tunnel",
            ["cloudflared", "tunnel", "run", "ai-stock"],
        )

        print("\n✅ 全部啟動完成")
        print("🌐 本機：http://127.0.0.1:5000")
        print("🌐 固定網址：https://app.ai966.online")
        print("📡 背景同步：workers/market_worker.py")
        print("📊 頁面：")
        print("   /        首頁")
        print("   /stock   個股分析")
        print("   /market  市場掃描")
        print("   /daily   今日策略")
        print("   /tools   進階工具")
        print("\n🛑 Ctrl + C 可停止全部\n")

        monitor()

    except KeyboardInterrupt:
        stop_all()
    except Exception as e:
        print(f"❌ run_all 發生錯誤：{e}")
        stop_all()


if __name__ == "__main__":
    main()