"""
Benchmark Service: Quantization Impact Calculation & Data Provider
===================================================================
คำนวณและสร้างรายงานการวิเคราะห์ผลกระทบของ Quantization สำหรับ Jinja2 Web UI & REST API
"""

import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

from app.models.ml_model import load_dataset_hybrid


def get_quantization_benchmark_data(csv_path: str = 'student_mental_health.csv') -> dict:
    """
    ประมวลผลการเปรียบเทียบ Quantization Scaling Factors vs Baseline Float64
    โดยดึงข้อมูลจาก Database (MySQL) เป็นหลัก พร้อม Fallback เป็น CSV
    """
    df, data_source_name, data_source_detail = load_dataset_hybrid(csv_path)
    feature_cols = ['Age', 'CGPA_Scaled', 'Depression', 'Anxiety', 'Panic_Attack', 'Seek_Treatment']
    X = df[feature_cols].values
    y = df['Target_Risk'].values

    # Train-Test Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 1. Baseline Model (Float64)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    raw_weights = model.coef_[0]
    raw_bias = float(model.intercept_[0])

    y_pred_baseline = model.predict(X_test)
    raw_scores_test = np.dot(X_test, raw_weights) + raw_bias

    base_acc = float(accuracy_score(y_test, y_pred_baseline))
    base_prec = float(precision_score(y_test, y_pred_baseline, zero_division=0))
    base_rec = float(recall_score(y_test, y_pred_baseline, zero_division=0))
    base_f1 = float(f1_score(y_test, y_pred_baseline, zero_division=0))

    baseline_info = {
        "accuracy_pct": round(base_acc * 100, 2),
        "precision": round(base_prec, 4),
        "recall": round(base_rec, 4),
        "f1_score": round(base_f1, 4),
        "weights": [round(float(w), 4) for w in raw_weights],
        "bias": round(raw_bias, 4),
        "total_samples": len(df),
        "test_samples": len(y_test),
        "data_source_name": data_source_name,
        "data_source_detail": data_source_detail
    }

    # 2. Scaling Factors Test
    scaling_factors = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000, 100000]
    rows = []

    # Add baseline row
    rows.append({
        "method": "Baseline (Float64)",
        "scaling_factor": "-",
        "scaling_val": 0,
        "accuracy_pct": round(base_acc * 100, 2),
        "precision": round(base_prec, 4),
        "recall": round(base_rec, 4),
        "f1_score": round(base_f1, 4),
        "delta_acc": 0.0,
        "mismatches": 0,
        "mae_drift": 0.0,
        "badge": "baseline",
        "badge_text": "Reference Baseline"
    })

    chart_labels = []
    chart_accuracy = []
    chart_mae = []

    for S in scaling_factors:
        q_weights = np.round(raw_weights * S).astype(np.int64)
        q_bias = round(raw_bias * S)

        quant_scores_test = np.dot(X_test, q_weights) + q_bias
        y_pred_quant = (quant_scores_test >= 0).astype(int)

        acc = float(accuracy_score(y_test, y_pred_quant))
        prec = float(precision_score(y_test, y_pred_quant, zero_division=0))
        rec = float(recall_score(y_test, y_pred_quant, zero_division=0))
        f1 = float(f1_score(y_test, y_pred_quant, zero_division=0))

        delta_acc = round((acc - base_acc) * 100, 2)
        mismatches = int(np.sum(y_pred_baseline != y_pred_quant))
        reconstructed_scores = quant_scores_test / S
        mae_drift = float(np.mean(np.abs(raw_scores_test - reconstructed_scores)))

        badge = "optimal"
        badge_text = "Optimal (No Loss)"
        if S == 1000:
            badge = "active-circuit"
            badge_text = "⭐ Selected in ZK Circuit"
        elif mismatches > 0:
            badge = "loss"
            badge_text = f"Loss ({mismatches} Mismatch)"

        rows.append({
            "method": f"Quantized (S={S})",
            "scaling_factor": f"{S:,}",
            "scaling_val": S,
            "accuracy_pct": round(acc * 100, 2),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "delta_acc": delta_acc,
            "mismatches": mismatches,
            "mae_drift": round(mae_drift, 6),
            "badge": badge,
            "badge_text": badge_text
        })

        chart_labels.append(f"S={S:,}")
        chart_accuracy.append(round(acc * 100, 2))
        chart_mae.append(round(mae_drift, 6))

    return {
        "baseline": baseline_info,
        "rows": rows,
        "chart_data": {
            "labels": chart_labels,
            "accuracy": chart_accuracy,
            "mae": chart_mae
        }
    }
