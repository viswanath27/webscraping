
from google.cloud.dialogflowcx_v3.services.test_cases.client import TestCasesClient
from google.cloud.dialogflowcx_v3.types.test_case import ListTestCaseResultsRequest


def list_test_case(project_id, agent_id, test_id, location):

    req = ListTestCaseResultsRequest()
    req.parent = f"projects/{project_id}/locations/{location}/agents/{agent_id}/testCases/{test_id}"
    req.filter = "environment=draft"
    client = TestCasesClient(
        client_options={"api_endpoint": f"{location}-dialogflow.googleapis.com"}
    )
    # Makes a call to list all test case results that match filter
    result = client.list_test_case_results(request=req)
    print(result)
    return result
