# 🚀 Deploy BankLead AI lên Google Cloud Run

Hướng dẫn triển khai app Streamlit lên **Google Cloud Run** (serverless,
trả tiền theo lượt dùng, tự động scale về 0 khi không có traffic).

## 0. Yêu cầu chuẩn bị

- Một **Google Cloud Project** (ví dụ `my-banklead-project`) đã bật billing.
- Cài **Google Cloud CLI** (`gcloud`): https://cloud.google.com/sdk/docs/install
- (Tùy chọn) Cài **Docker** nếu muốn build local.

```bash
# Đăng nhập và chọn project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

## 1. File cấu hình đã có sẵn trong repo

| File | Vai trò |
|---|---|
| `Dockerfile` | Đóng gói app thành container, chạy Streamlit trên `$PORT` |
| `.dockerignore` | Loại bỏ file thừa khỏi image (nhẹ hơn) |
| `.gcloudignore` | Loại bỏ file thừa khi upload lên Cloud Build |

**Điểm mấu chốt cho Cloud Run** — Cloud Run *bắt buộc* container phải lắng
nghe trên cổng lấy từ biến môi trường `$PORT` (mặc định `8080`) và bind vào
`0.0.0.0`. Dockerfile đã cấu hình đúng:

```dockerfile
ENV PORT=8080
CMD streamlit run app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
```

## 2. Bật các API cần thiết (chạy 1 lần)

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
```

Giải thích: `run` (Cloud Run), `cloudbuild` (build image trên cloud),
`artifactregistry` (nơi lưu image).

---

## Cách A — Deploy nhanh nhất (1 lệnh, build trên cloud) ⭐ Khuyến nghị

`gcloud run deploy` sẽ tự build image từ `Dockerfile` bằng Cloud Build, đẩy
vào Artifact Registry, rồi deploy lên Cloud Run — tất cả trong một lệnh.

```bash
gcloud run deploy banklead-ai \
    --source . \
    --region asia-southeast1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --port 8080 \
    --min-instances 0 \
    --max-instances 3
```

Giải thích từng cờ:
- `banklead-ai` — tên service trên Cloud Run.
- `--source .` — build từ thư mục hiện tại (dùng `Dockerfile`).
- `--region asia-southeast1` — Singapore (gần Việt Nam, độ trễ thấp).
- `--allow-unauthenticated` — cho phép truy cập công khai (bỏ cờ này nếu
  muốn yêu cầu đăng nhập Google).
- `--memory 1Gi` — Streamlit + scikit-learn + XGBoost cần ~1GB RAM.
- `--min-instances 0` — scale về 0 khi rảnh ⇒ không tốn tiền lúc không dùng.
- `--max-instances 3` — giới hạn chi phí khi tải cao.

Sau khi chạy xong, gcloud in ra **Service URL**, dạng:
`https://banklead-ai-xxxxxxxx-as.a.run.app` → mở trên trình duyệt là dùng được.

---

## Cách B — Build thủ công với Artifact Registry (kiểm soát chi tiết hơn)

```bash
# 1. Tạo một Docker repository trong Artifact Registry (chạy 1 lần)
gcloud artifacts repositories create banklead-repo \
    --repository-format=docker \
    --location=asia-southeast1 \
    --description="BankLead AI images"

# 2. Đặt biến cho gọn
export PROJECT_ID=$(gcloud config get-value project)
export IMAGE=asia-southeast1-docker.pkg.dev/$PROJECT_ID/banklead-repo/banklead-ai:v1

# 3. Build image bằng Cloud Build và đẩy lên registry
gcloud builds submit --tag $IMAGE

# 4. Deploy image vừa build lên Cloud Run
gcloud run deploy banklead-ai \
    --image $IMAGE \
    --region asia-southeast1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi --cpu 1 --port 8080 \
    --min-instances 0 --max-instances 3
```

### (Tùy chọn) Build & test bằng Docker ở máy local trước

```bash
# Build image
docker build -t banklead-ai:local .

# Chạy thử, mô phỏng biến PORT của Cloud Run
docker run --rm -p 8080:8080 -e PORT=8080 banklead-ai:local
# Mở http://localhost:8080
```

---

## 3. Cập nhật app sau khi sửa code

Chỉ cần chạy lại lệnh deploy (Cách A) — Cloud Run tạo *revision* mới và
chuyển traffic sang đó:

```bash
gcloud run deploy banklead-ai --source . --region asia-southeast1
```

## 4. Xem log / quản lý

```bash
# Xem URL của service
gcloud run services describe banklead-ai --region asia-southeast1 \
    --format='value(status.url)'

# Xem log realtime
gcloud run services logs tail banklead-ai --region asia-southeast1

# Xóa service khi không dùng nữa
gcloud run services delete banklead-ai --region asia-southeast1
```

## 5. Lưu ý về chi phí & dữ liệu

- Cloud Run tính tiền theo CPU/RAM × thời gian xử lý request. `--min-instances 0`
  giúp **gần như $0** khi không ai dùng (chỉ trả khi có truy cập).
- Container Cloud Run **không lưu trạng thái** (ephemeral): dữ liệu CSV người
  dùng upload và mô hình đã train chỉ tồn tại trong phiên (`st.session_state`).
  Khi instance bị thu hồi, dữ liệu mất — điều này đúng với thiết kế demo của app.
- Nếu cần lưu lâu dài (lịch sử lead, mô hình), hãy gắn thêm Cloud Storage hoặc
  một database — thuộc phạm vi nâng cấp tương lai.
