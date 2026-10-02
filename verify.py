import numpy as np
import pandas as pd
import joblib
import os

FEATURE_COLUMNS = [
    "flow_duration", "Header_Length", "Protocol Type", "Duration",
    "Rate", "Srate", "Drate", "fin_flag_number", "syn_flag_number",
    "rst_flag_number", "psh_flag_number", "ack_flag_number", "ece_flag_number",
    "cwr_flag_number", "ack_count", "syn_count", "fin_count", "urg_count",
    "rst_count", "HTTP", "HTTPS", "DNS", "Telnet", "SMTP", "SSH", "IRC",
    "TCP", "UDP", "DHCP", "ARP", "ICMP", "IPv", "LLC", "Tot sum",
    "Min", "Max", "AVG", "Std", "Tot size", "IAT", "Number",
    "Magnitue", "Radius", "Covariance", "Variance", "Weight"
]

def check_files():
    required = [
        "scaler_standard.pkl",
        "pca_quantum_reducer.pkl",
        "quantum_feature_transformer.pkl",
        "binary_model.pkl",
        "multi_model.pkl",
        "label_encoder.pkl",
        "model_metrics.pkl"
    ]
    all_found = True
    for f in required:
        if os.path.exists(f):
            print(f"  [OK] {f}")
        else:
            print(f"  [MISSING] {f}")
            all_found = False
    return all_found

def load_components():
    scaler = joblib.load("scaler_standard.pkl")
    pca = joblib.load("pca_quantum_reducer.pkl")
    qt = joblib.load("quantum_feature_transformer.pkl")
    binary_model = joblib.load("binary_model.pkl")
    multi_model = joblib.load("multi_model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    metrics = joblib.load("model_metrics.pkl")
    print("  [OK] All components loaded")
    print(f"  [OK] Classes: {list(label_encoder.classes_)}")
    return scaler, pca, qt, binary_model, multi_model, label_encoder, metrics

def predict_row(row_values, scaler, pca, qt, binary_model, multi_model, label_encoder):
    x = np.array(row_values).reshape(1, -1)
    x_scaled = scaler.transform(x)
    x_pca = pca.transform(x_scaled)
    x_qe = qt.transform(x_pca)
    binary_pred = int(binary_model.predict(x_qe)[0])
    binary_proba = float(binary_model.predict_proba(x_qe)[0][1])
    multi_pred = int(multi_model.predict(x_qe)[0])
    multi_proba = multi_model.predict_proba(x_qe)[0]
    attack_type = label_encoder.inverse_transform([multi_pred])[0]
    confidence = float(multi_proba.max())
    is_attack = binary_pred == 1
    return binary_proba, is_attack, attack_type, confidence

def run_on_simulation_csv(scaler, pca, qt, binary_model, multi_model, label_encoder):
    csv_path = "datasets/simulation/sim_1.csv"
    if not os.path.exists(csv_path):
        print("  [SKIP] sim_1.csv not found")
        return

    df = pd.read_csv(csv_path)
    correct_binary = 0
    correct_multi = 0
    total = len(df)

    for _, row in df.iterrows():
        features = row[FEATURE_COLUMNS].values.astype(float).tolist()
        actual_binary = int(row["is_attack"])
        actual_type = row["label"]
        binary_proba, is_attack, attack_type, confidence = predict_row(
            features, scaler, pca, qt, binary_model, multi_model, label_encoder
        )
        if int(is_attack) == actual_binary:
            correct_binary += 1
        if attack_type == actual_type:
            correct_multi += 1

    print(f"  [OK] Binary accuracy:     {correct_binary}/{total} ({correct_binary/total*100:.1f}%)")
    print(f"  [OK] Multi-class accuracy: {correct_multi}/{total} ({correct_multi/total*100:.1f}%)")

def main():
    print("\n--- FILE CHECK ---")
    if not check_files():
        print("\n[FAILED] Missing files. Aborting.")
        return

    print("\n--- LOADING COMPONENTS ---")
    try:
        scaler, pca, qt, binary_model, multi_model, label_encoder, metrics = load_components()
    except Exception as e:
        print(f"  [FAILED] {e}")
        return

    print("\n--- MODEL METRICS ---")
    print(f"  Binary  — Accuracy: {metrics['binary']['accuracy']:.4f} | F1: {metrics['binary']['f1']:.4f}")
    print(f"  Multi   — Accuracy: {metrics['multi']['accuracy']:.4f} | F1: {metrics['multi']['f1']:.4f}")
    print(f"  Quantum — Qubits: {metrics['quantum_config']['n_qubits']} | Feature Map: {metrics['quantum_config']['feature_map']}")

    print("\n--- SINGLE ROW PREDICTION (BENIGN) ---")
    try:
        benign_row = [
            27.676, 2232967.2, 6.0, 114.4, 79.110, 79.110, 0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 0.0, 2.0, 0.0, 77.0, 2188.5, 0.0,
            1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 1.0, 11828.2, 66.0, 1514.0, 756.786, 714.776, 1079.6,
            166526165.47, 13.5, 38.788, 1011.217, 511297.954, 1.0, 244.6
        ]
        binary_proba, is_attack, attack_type, confidence = predict_row(
            benign_row, scaler, pca, qt, binary_model, multi_model, label_encoder
        )
        print(f"  Score: {binary_proba:.4f} | Attack: {is_attack} | Type: {attack_type} | Confidence: {confidence:.4f}")
        print(f"  Expected: Normal/BenignTraffic")
    except Exception as e:
        print(f"  [FAILED] {e}")

    print("\n--- SINGLE ROW PREDICTION (ATTACK - DDoS-SYN_Flood) ---")
    try:
        attack_row = [
            0.0, 54.0, 6.0, 64.0, 2.393, 2.393, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 1.0, 567.0, 54.0, 54.0, 54.0, 0.0, 54.0,
            83093265.31, 9.5, 10.392, 0.0, 0.0, 0.0, 141.55
        ]
        binary_proba, is_attack, attack_type, confidence = predict_row(
            attack_row, scaler, pca, qt, binary_model, multi_model, label_encoder
        )
        print(f"  Score: {binary_proba:.4f} | Attack: {is_attack} | Type: {attack_type} | Confidence: {confidence:.4f}")
        print(f"  Expected: Attack/DDoS-SYN_Flood")
    except Exception as e:
        print(f"  [FAILED] {e}")

    print("\n--- CSV BATCH TEST (sim_1.csv) ---")
    try:
        run_on_simulation_csv(scaler, pca, qt, binary_model, multi_model, label_encoder)
    except Exception as e:
        print(f"  [FAILED] {e}")

    print("\n--- VERIFY COMPLETE ---\n")

if __name__ == "__main__":
    main()