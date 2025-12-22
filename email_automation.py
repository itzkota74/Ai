def send_email(to_email, subject, body):
    # Mock: prints to console instead of sending email
    print(f"[Mock Email] To: {to_email} | Subject: {subject}\n{body}\n")

# Test sending
send_email("user@example.com", "Welcome to your affiliate page!", "Click the link to start: https://example.com")
