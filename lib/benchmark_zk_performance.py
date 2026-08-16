"""
CLI Tool: Cryptographic & ZK-SNARKs Performance Benchmark
=========================================================
รันการทดสอบและวิเคราะห์ประสิทธิภาพเชิงรหัสวิทยาของ Noir ZK Circuit
- ACIR Opcodes & Constraint Complexity
- Latency Distribution Profiling (Min, Mean, Median, P95, P99, Jitter)
- Feature Scaling Complexity O(N)

วิธีรัน:
python lib/benchmark_zk_performance.py
"""

import sys
import os
import asyncio
import pandas as pd

# Root Directory setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.services.zk_benchmark_service import run_cryptographic_benchmark


async def main():
    print("=" * 80)
    print("🔬 กำลังเริ่มการทดลอง: CRYPTOGRAPHIC & ZK PERFORMANCE BENCHMARK")
    print("=" * 80)

    data = await run_cryptographic_benchmark(iterations=30)
    summary = data["summary"]

    print("\n📊 [1] SUMMARY STATISTICAL METRICS (PROVER LATENCY & CONSTRAINTS)")
    print(f"   • Total Test Iterations     : {summary['iterations']} runs")
    print(f"   • ACIR Circuit Constraints  : {summary['acir_opcodes']} Opcodes")
    print(f"   • Brillig Gates             : {summary['brillig_opcodes']} Opcodes")
    print(f"   • Mean Proving Latency      : {summary['mean_latency_ms']} ms")
    print(f"   • Median Latency (P50)      : {summary['median_latency_ms']} ms")
    print(f"   • 95th Percentile (P95)     : {summary['p95_latency_ms']} ms")
    print(f"   • Min / Max Latency         : {summary['min_latency_ms']} ms / {summary['max_latency_ms']} ms")
    print(f"   • Jitter (Standard Deviation): ±{summary['std_jitter_ms']} ms")
    print(f"   • Prover Success Pass Rate  : {summary['pass_rate_pct']}%")
    print(f"   • Theoretical Throughput    : {summary['theoretical_throughput_rps']} Req/sec")

    print("\n⚙️ [2] CIRCUIT CONSTRAINT ALLOCATION BREAKDOWN")
    df_breakdown = pd.DataFrame(data["circuit_breakdown"])
    print(df_breakdown.to_string(index=False))

    print("\n📐 [3] FEATURE SCALING COMPLEXITY SIMULATION (O(N) ASYMPTOTIC ANALYSIS)")
    df_scaling = pd.DataFrame(data["scaling_data"])
    print(df_scaling.to_string(index=False))

    # Save to CSV
    output_csv = "zk_performance_benchmark_results.csv"
    df_scaling.to_csv(output_csv, index=False)
    print(f"\n💾 บันทึกผลการทดลอง Scaling เรียบร้อยที่: {output_csv}")


if __name__ == '__main__':
    asyncio.run(main())
