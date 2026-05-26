from listmonk_api.api.api_client_base import BaseApiClient


class ListmonkAPI(BaseApiClient):
    def get_templates(self, max_pages: int = 0, per_page: int = 100):
        response = self.get(f"/templates?per_page={per_page}")
        total_pages = int(response.headers.get("X-Total-Pages", 1))

        results = []
        template_filter = f"?per_page={per_page}"

        if max_pages == 0 or max_pages > total_pages:
            max_pages = total_pages

        for page in range(1, max_pages + 1):
            response_page = self.get(f"/templates{template_filter}&page={page}")
            response_json = response_page.json()
            if isinstance(response_json, dict) and "data" in response_json:
                results.extend(response_json["data"].get("results", []))
            elif isinstance(response_json, list):
                results.extend(response_json)
            else:
                results.append(response_json)

        return results

    def get_template(self, template_id: int):
        return self.get(f"/templates/{template_id}").json()

    def get_template_preview(self, template_id: int):
        return self.get(f"/templates/{template_id}/preview").json()

    def set_default_template(self, template_id: int):
        return self.put(f"/templates/{template_id}/default").json()

    def delete_template(self, template_id: int):
        return self.delete(f"/templates/{template_id}").json()

    # ------------------------------------------------------------------------------------------------------------------
    # Transactional API
    # ------------------------------------------------------------------------------------------------------------------
