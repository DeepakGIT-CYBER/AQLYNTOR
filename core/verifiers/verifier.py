from pathlib import Path

class OutcomeVerifier:
    @staticmethod
    def verify_file_exists(file_path: str, required_headings: list[str] = None) -> tuple[bool, str]:
        path = Path(file_path)
        if not path.exists():
            return False, f"Verification failed: File {file_path} does not exist."
        if required_headings:
            content = path.read_text(encoding="utf-8")
            for heading in required_headings:
                if heading not in content:
                    return False, f"Verification failed: Required section '{heading}' missing."
        return True, "Outcome verified successfully."