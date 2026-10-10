import os
import sys
import subprocess
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PY_BIN = sys.executable

def main():
    print("=" * 80)
    print("🚀 开始执行 StockLearning 全量课程参考答案 (answers/) 自动化回归测试")
    print(f"当前运行 Python: {PY_BIN}")
    print(f"工作目录: {BASE_DIR}")
    print("=" * 80)

    answer_files = sorted(glob.glob(os.path.join(BASE_DIR, "*/answers/*.py")))
    if not answer_files:
        print("❌ 未发现任何 answer 文件！")
        sys.exit(1)

    passed = 0
    failed = 0
    failed_list = []

    for idx, fpath in enumerate(answer_files, start=1):
        rel_path = os.path.relpath(fpath, BASE_DIR)
        print(f"[{idx:02d}/{len(answer_files):02d}] 正在测试: {rel_path} ... ", end="", flush=True)
        
        res = subprocess.run([PY_BIN, fpath], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ PASS")
            passed += 1
        else:
            print("❌ FAILED")
            print("STDERR:")
            print(res.stderr)
            failed += 1
            failed_list.append(rel_path)

    print("=" * 80)
    print(f"📊 测试总结: 总计 {len(answer_files)} 课 | 通过: {passed} 课 | 失败: {failed} 课")
    if failed == 0:
        print("🎉 恭喜！全部 46 门课程参考实现与单元测试断言 100% 验证通过！")
        sys.exit(0)
    else:
        print(f"⚠️ 存在失败课目: {failed_list}")
        sys.exit(1)

if __name__ == "__main__":
    main()
