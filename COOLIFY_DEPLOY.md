# Deploy Sphinx Net ke Coolify dengan Domain sphinxnet.nexawebs.com

## 📋 Prasyarat Repository

Pastikan semua file ini ada di repository Git Anda:
- `Dockerfile` - Build configuration
- `docker-compose.yml` - Satu file compose untuk semua environment
- `nginx/nginx.conf` - Konfigurasi Nginx utama
- `nginx/sites-available/sphinxnet.conf` - Virtual host config
- `.env.example` - Template environment variables
- `.dockerignore` - File yang diabaikan Docker

## 🚀 Langkah 1: Push ke Repository

```bash
git add .
git commit -m "Add Docker configuration for Coolify deployment"
git push origin main
```

## 🎯 Langkah 2: Setup di Coolify

### 1. Connect Repository
- Login ke dashboard Coolify
- **Add New Resource** > **Git Repository**
- Connect repository Git Anda
- Pilih branch `main`

### 2. Configure Application
- **Application Name**: Sphinx Net App
- **Source**: Git Repository
- **Docker Compose File**: `docker-compose.yml`
- **Auto-Deploy**: Enable ✅

### 3. Environment Variables
Tambahkan di Coolify:

```bash
# Domain Configuration
COOLIFY_DOMAIN_0_DOMAIN=sphinxnet.nexawebs.com

# Security
COOLIFY_SECRET_KEY=buat-secret-key-random-disini

# Optional: Override defaults
# CORS_ORIGINS=https://sphinxnet.nexawebs.com,http://localhost:3000
# SECRET_KEY=custom-secret-key
```

### 4. Domain & SSL Setup
- **Domain**: `sphinxnet.nexawebs.com`
- **SSL**: Auto-enable dengan Let's Encrypt
- Coolify otomatis mengatur Traefik & SSL certificates

## 🔥 Langkah 3: Deploy

### Manual Deploy
1. Klik **Deploy** di dashboard Coolify
2. Tunggu proses build dan deploy selesai
3. Monitor logs untuk melihat progress

### Auto-Deploy
✅ Sudah di-enable - Setiap push ke branch `main` akan trigger auto-deploy

## ✅ Langkah 4: Verifikasi Deployment

Setelah deploy selesai, test:

1. **API Health Check**:
   ```
   https://sphinxnet.nexawebs.com/api/health
   ```
   → Harus merespon `OK` dengan status 200

2. **Frontend**:
   ```
   https://sphinxnet.nexawebs.com/
   ```
   → Harus menampilkan halaman utama Sphinx Net

3. **Test Survey**:
   - Klik "Survey Pengguna"
   - Isi survey
   - Pastikan API recommendations berfungsi

## 🚨 Troubleshooting

### Build Gagal?
- Pastikan `hybrid_ml_survey_server.py` ada di folder `backend/`
- Cek semua Python dependencies di `Dockerfile`
- Lihat build logs di Coolify dashboard

### SSL/TLS Error?
- Coolify auto-generate SSL dengan Let's Encrypt
- Pastikan domain `sphinxnet.nexawebs.com` sudah pointing ke IP server Coolify
- Tunggu beberapa menit untuk SSL propagation

### API Tidak Responding?
- Cek health check logs
- Pastikan port 5000 tidak diblokir firewall
- Verify environment variables ter-set dengan benar

### Database Issues?
- Volume `sphinxnet_data` sudah di-mount
- Database akan otomatis dibuat di `/app/data`
- Logs tersimpan di volume `sphinxnet_logs`

## 📊 Monitoring

Coolify provides:
- ✅ Real-time logs untuk setiap service
- ✅ Resource monitoring (CPU, Memory)
- ✅ Deploy history
- ✅ Health check status
- ✅ SSL certificate management

## 🔐 Security Notes

1. **Environment Variables**:
   - ✅ Sudah menggunakan Coolify secrets (`COOLIFY_SECRET_KEY`)
   - ❌ Jangan commit secrets ke Git

2. **Network Security**:
   - ✅ Traefik sebagai reverse proxy
   - ✅ Auto HTTPS redirection
   - ✅ Security headers sudah dikonfigurasi

3. **Best Practices**:
   - Regular update base image
   - Monitor CVEs di dependencies
   - Backup data secara berkala

## 🔄 Update & Maintenance

### Update Application
```bash
git add .
git commit -m "Update: description"
git push origin main
# Coolify auto-deploy! ✅
```

### Configuration Changes
Edit environment variables di Coolify dashboard → Auto-reload

### Rollback
Pilih deploy sebelumnya di Coolify dashboard → Rollback

---

**🎉 Your Sphinx Net application is now ready for production on Coolify!**