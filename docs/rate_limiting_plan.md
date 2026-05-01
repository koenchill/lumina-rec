# Rate Limiting Plan

## Purpose

This document defines the rate limiting approach for Lumina Rec.

## Current State

Lumina Rec uses application level rate limiting through SlowAPI.

Current local value:

```env
LUMINA_RATE_LIMIT=300/minute