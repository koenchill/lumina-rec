# Known Issues

## Purpose

This file tracks known issues and limitations.

## Known Issues

| Issue | Impact | Current Workaround |
|---|---|---|
| Local API key only | Not production grade authentication | Replace with JWT or API gateway later |
| Metrics endpoint open locally | Could expose operational details if deployed publicly | Restrict metrics in production |
| Model selected by run ID | Manual promotion process | Add MLflow Model Registry alias |
| No dataset checksum yet | Dataset integrity not fully verified | Add dataset checksum validation |
| No artifact manifest yet | Mismatched artifacts may be harder to detect | Add artifact manifest validation |
| RMSE only | Ranking quality not fully measured | Add Precision at K, Recall at K, and NDCG |
| No production deployment yet | Local only | Add Terraform and cloud deployment path |
| No centralized logs | Local logs only | Add production log platform later |
| No managed secrets | `.env` used locally | Add managed secret store later |