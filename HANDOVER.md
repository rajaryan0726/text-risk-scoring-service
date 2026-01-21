# Text Risk Scoring Service - Operational Handover

[![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)]()
[![Maintenance](https://img.shields.io/badge/maintenance-Active-brightgreen.svg)]()
[![Documentation](https://img.shields.io/badge/docs-Complete-blue.svg)]()

This document provides comprehensive operational guidance for maintaining, deploying, and troubleshooting the Text Risk Scoring Service.

## 📋 Table of Contents

- [Service Overview](#service-overview)
- [System Requirements](#system-requirements)
- [Deployment Guide](#deployment-guide)
- [Configuration Management](#configuration-management)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Maintenance Procedures](#maintenance-procedures)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Backup & Recovery](#backup--recovery)
- [Contact Information](#contact-information)

## 🎯 Service Overview

### Purpose
The Text Risk Scoring Service is a deterministic API that analyzes text content and assigns risk scores based on keyword-based rules. It's designed for demo environments, evaluation tasks, and moderation pipelines.

### Key Characteristics
- **Deterministic**: Same input always produces same output
- **Stateless**: No database or persistent storage required
- **Lightweight**: Minimal resource requirements
- **Self-contained**: No external API dependencies

### Service Endpoints
- **Primary**: `POST /analyze` - Text risk analysis
- **Health**: `GET /health` - Service health check
- **Docs**: `GET /docs` - Interactive API documentation
- **OpenAPI**: `GET /openapi.json` - API specification

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.10 or higher
- **RAM**: 512MB available memory
- **CPU**: 1 core (2+ recommended)
- **Disk**: 100MB free space

### Recommended Production Requirements
- **OS**: Ubuntu 20.04 LTS or Windows Server 2019+
- **Python**: 3.11+
- **RAM**: 2GB available memory
- **CPU**: 2+ cores
- **Disk**: 1GB free space
- **Network**: Stable internet connection for package updates

### Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

## 🚀 Deployment Guide

### Local Development Deployment

1. **Environment Setup**
   ```bash
   # Clone repository
   git clone https://github.com/rajaryan0726/text-risk-scoring-service.git
   cd text-risk-scoring-service
   
   # Create virtual environment
   python -m venv venv
   
   # Activate environment (Windows)
   venv\Scripts\activate
   
   # Activate environment (macOS/Linux)
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start Service**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify Deployment**
   ```bash
   curl -X POST "http://localhost:8000/analyze" \
        -H "Content-Type: application/json" \
        -d '{"text": "test message"}'
   ```

### Production Deployment

#### Option 1: Direct Python Deployment
```bash
# Production server startup
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Option 2: Docker Deployment (Future)
```dockerfile
# Dockerfile (to be created)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 3: Cloud Deployment
- **AWS**: Deploy using AWS Lambda or ECS
- **Azure**: Use Azure Container Instances or App Service
- **GCP**: Deploy on Cloud Run or Compute Engine

## ⚙️ Configuration Management

### Environment Variables
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info

# Application Configuration
MAX_TEXT_LENGTH=10000
DEFAULT_RISK_THRESHOLD=0.5
ENABLE_DETAILED_LOGGING=true
```

### Configuration Files
The service uses minimal configuration. Key settings are in:
- `app/engine.py` - Risk scoring rules and thresholds
- `app/schemas.py` - Input/output validation rules

### Customizing Risk Rules
To modify risk detection rules, edit `app/engine.py`:

```python
# Example: Adding new risk keywords
FRAUD_KEYWORDS = [
    "scam", "fraud", "phishing", "fake", "counterfeit",
    # Add new keywords here
]

# Example: Adjusting risk thresholds
def _calculate_risk_category(self, score: float) -> str:
    if score >= 0.7:  # Adjust threshold
        return "HIGH"
    elif score >= 0.3:  # Adjust threshold
        return "MEDIUM"
    return "LOW"
```

## 📊 Monitoring & Health Checks

### Health Check Endpoint
```bash
# Basic health check
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### Key Metrics to Monitor
- **Response Time**: Should be < 100ms for typical requests
- **Error Rate**: Should be < 1% under normal conditions
- **Memory Usage**: Should remain stable over time
- **CPU Usage**: Should be < 50% under normal load

### Logging
The service logs to stdout. Key log events:
- Service startup/shutdown
- Request processing errors
- Invalid input handling
- Performance warnings

### Monitoring Setup
```bash
# Enable detailed logging
export LOG_LEVEL=debug
uvicorn app.main:app --log-level debug

# Monitor logs in real-time
tail -f /var/log/text-risk-service.log
```

## 🔧 Troubleshooting Guide

### Common Issues

#### Issue 1: Service Won't Start
**Symptoms**: ImportError, ModuleNotFoundError
**Solution**:
```bash
# Verify Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for conflicting packages
pip list | grep fastapi
```

#### Issue 2: High Memory Usage
**Symptoms**: Memory consumption grows over time
**Solution**:
```bash
# Restart service periodically
# Monitor with: ps aux | grep uvicorn

# Check for memory leaks in custom code
# Review app/engine.py for object retention
```

#### Issue 3: Slow Response Times
**Symptoms**: Requests taking > 1 second
**Solution**:
```bash
# Check system resources
top -p $(pgrep -f uvicorn)

# Optimize text processing
# Review large text inputs in logs

# Consider adding request size limits
```

#### Issue 4: Invalid JSON Responses
**Symptoms**: Malformed API responses
**Solution**:
```bash
# Verify Pydantic schemas
python -c "from app.schemas import RiskAnalysisResponse; print('OK')"

# Check for encoding issues
# Ensure UTF-8 encoding for all text inputs
```

### Debug Mode
```bash
# Run in debug mode
uvicorn app.main:app --reload --log-level debug

# Enable Python debugging
export PYTHONPATH=.
python -m pdb -c continue app/main.py
```

### Log Analysis
```bash
# Search for errors
grep -i error /var/log/text-risk-service.log

# Monitor request patterns
grep "POST /analyze" /var/log/text-risk-service.log | tail -20

# Check response times
grep "completed" /var/log/text-risk-service.log | awk '{print $NF}'
```

## 🔄 Maintenance Procedures

### Regular Maintenance Tasks

#### Daily
- [ ] Check service health status
- [ ] Review error logs
- [ ] Monitor resource usage

#### Weekly
- [ ] Update dependencies (if needed)
- [ ] Run full test suite
- [ ] Review performance metrics
- [ ] Check disk space

#### Monthly
- [ ] Security updates
- [ ] Performance optimization review
- [ ] Documentation updates
- [ ] Backup verification

### Update Procedures

#### Dependency Updates
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all packages (use caution)
pip install --upgrade -r requirements.txt

# Test after updates
python -m pytest
```

#### Code Updates
```bash
# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Restart service
# (Use process manager or manual restart)
```

### Rollback Procedures
```bash
# Rollback to previous version
git checkout <previous-commit-hash>

# Reinstall dependencies
pip install -r requirements.txt

# Restart service
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔐 Security Considerations

### Current Security Status
- ✅ No authentication required (by design)
- ✅ Input validation via Pydantic
- ✅ No external API calls
- ✅ No persistent data storage
- ⚠️ No rate limiting implemented
- ⚠️ No request size limits

### Security Recommendations

#### Input Validation
- Text length is limited in schemas
- Special characters are handled safely
- No code execution from user input

#### Network Security
```bash
# Run on specific interface
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Use reverse proxy (nginx/Apache)
# Configure SSL/TLS termination
# Implement rate limiting at proxy level
```

#### Monitoring
- Log all requests for audit trail
- Monitor for unusual patterns
- Set up alerts for high error rates

### Future Security Enhancements
- API key authentication
- Request rate limiting
- Input sanitization improvements
- Security headers implementation

## ⚡ Performance Optimization

### Current Performance
- **Response Time**: ~50ms for typical requests
- **Throughput**: ~100 requests/second (single worker)
- **Memory Usage**: ~50MB baseline
- **CPU Usage**: Minimal for text processing

### Optimization Strategies

#### Scaling Options
```bash
# Increase workers
uvicorn app.main:app --workers 4

# Use process manager
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Caching (Future Enhancement)
```python
# Example: Response caching for identical inputs
from functools import lru_cache

@lru_cache(maxsize=1000)
def analyze_text_cached(text_hash: str) -> dict:
    # Implementation would go here
    pass
```

#### Resource Monitoring
```bash
# Monitor resource usage
htop
iostat 1
vmstat 1

# Profile Python application
python -m cProfile -o profile.stats app/main.py
```

## 💾 Backup & Recovery

### What to Backup
- Source code (version controlled in Git)
- Configuration files
- Custom risk rules (if modified)
- Deployment scripts
- Documentation

### Backup Procedures
```bash
# Code backup (Git)
git push origin main

# Configuration backup
tar -czf config-backup-$(date +%Y%m%d).tar.gz app/

# Full system backup
rsync -av /path/to/service/ /backup/location/
```

### Recovery Procedures
```bash
# Restore from Git
git clone https://github.com/rajaryan0726/text-risk-scoring-service.git

# Restore configuration
tar -xzf config-backup-YYYYMMDD.tar.gz

# Reinstall and restart
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Disaster Recovery
1. **Service Down**: Restart from backup location
2. **Data Corruption**: Restore from Git repository
3. **Server Failure**: Deploy on new server using this guide
4. **Complete Loss**: Rebuild from documentation and Git

## 📞 Contact Information

### Primary Contacts
- **Developer**: Raja Ryan (rajaryan0726@gmail.com)
- **Repository**: https://github.com/rajaryan0726/text-risk-scoring-service

### Support Escalation
1. **Level 1**: Check this documentation
2. **Level 2**: Review GitHub issues
3. **Level 3**: Contact developer directly

### Emergency Procedures
- **Service Critical**: Restart service immediately
- **Security Issue**: Take service offline, contact developer
- **Data Issue**: No persistent data, restart resolves most issues

---

## 📝 Handover Checklist

### For New Team Members
- [ ] Read this entire document
- [ ] Set up local development environment
- [ ] Run all tests successfully
- [ ] Deploy service locally
- [ ] Test API endpoints
- [ ] Review code structure
- [ ] Understand risk scoring logic
- [ ] Practice troubleshooting procedures

### For Operations Team
- [ ] Understand deployment procedures
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Test backup/recovery procedures
- [ ] Document any environment-specific configurations
- [ ] Establish maintenance schedule

### Knowledge Transfer Complete ✅
- [ ] All documentation reviewed
- [ ] Service successfully deployed
- [ ] Monitoring configured
- [ ] Team trained on procedures
- [ ] Emergency contacts established

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Next Review**: March 2024

> 💡 **Note**: This service is designed to be simple and reliable. When in doubt, restart the service - it's stateless and will recover quickly.