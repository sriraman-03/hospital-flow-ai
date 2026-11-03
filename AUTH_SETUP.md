# Hospital Flow AI — Login Setup

The project now includes one login screen with three role-based accounts:

- **Admin** — access to every application page.
- **Hospital Operations Manager** — dashboard, patient operations, resource management, notifications and agent workflow.
- **Clinical Staff** — dashboard, patient registration/queue, bed allocation, department routing and discharge/transfer pages.

## Configure credentials

1. Open the project folder in VS Code.
2. Open the existing `.env` file. **Do not delete your existing Gemini API key or model settings.**
3. Copy the six `HF_*` username/password settings from `.env.example` into the existing `.env` file.
4. Replace each sample password with a different strong password of your choice.
5. Save `.env` and restart Streamlit.

Example variable names (set your own values):

```env
HF_ADMIN_USERNAME=admin
HF_ADMIN_PASSWORD=your_admin_password
HF_MANAGER_USERNAME=operations
HF_MANAGER_PASSWORD=your_operations_password
HF_CLINICAL_USERNAME=clinical
HF_CLINICAL_PASSWORD=your_clinical_password
```

Start the application as usual:

```powershell
python -m streamlit run app.py
```

The login role determines which navigation pages are displayed. Logging out returns the user to the login screen.

## Important security note

This is an academic Streamlit prototype. Credentials are read from the local environment file and should not be committed or shared. The role restrictions are application-interface controls, not a substitute for production-grade identity management, server-side authorization, audit logging, or healthcare data security. Use demonstration data only; do not enter real patient information.

## Existing workflows

The login layer is added in `app.py` with credential handling in `auth.py`. The LangGraph, MCP, A2A, database, and patient/bed workflow modules are left unchanged.
