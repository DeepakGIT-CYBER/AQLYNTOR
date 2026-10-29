import os

class OutcomeVerifier:
    def verify_file_exists(self, file_path: str, min_bytes: int = 1) -> tuple[bool, str]:
        if not os.path.exists(file_path):
            return False, f"VERIFICATION FAILED: Target file '{file_path}' does not exist."
        
        file_size = os.path.getsize(file_path)
        if file_size < min_bytes:
            return False, f"VERIFICATION FAILED: File size ({file_size} bytes) is below threshold."

        return True, f"VERIFIED: File '{file_path}' exists ({file_size} bytes)."

    def verify_content_contains(self, file_path: str, required_keyword: str) -> tuple[bool, str]:
        exists, msg = self.verify_file_exists(file_path)
        if not exists:
            return False, msg

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if required_keyword not in content:
            return False, f"VERIFICATION FAILED: Required signature '{required_keyword}' missing."

        return True, f"VERIFIED: Found required signature '{required_keyword}'."
