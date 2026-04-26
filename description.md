# Pattern Printer

Pattern Printer is a small full-stack text pattern generator. It exposes a JSON API for rendering 31 reusable pattern types and ships with a browser UI for choosing symbols, dimensions, and pattern categories.

The backend validates every requested dimension before rendering so invalid input returns predictable API errors instead of silently clamping values or crashing the server.
