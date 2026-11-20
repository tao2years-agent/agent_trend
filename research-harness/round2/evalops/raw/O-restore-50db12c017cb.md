> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://www.comet.com/docs/opik/llms.txt.

# Set prompt version environment

PATCH http://localhost:5173/api/v1/private/prompts/versions/{versionId}/environments
Content-Type: application/json

Set or clear the environment owned by a prompt version.
Setting a non-null environment moves ownership atomically: any previous owner of that
environment for the same prompt has its environment cleared in the same transaction.
Setting null clears the environment from the version.
The environment must already exist in the workspace registry; unknown names return 404.


Reference: https://www.comet.com/docs/opik/reference/rest-api/prompts/set-prompt-version-environment

## Servers

- `http://localhost:5173/api` (Local server, default)
- `https://www.comet.com/opik/api` (Opik Cloud)

## Request

### Path parameters

- `versionId` (string, required)

### Body (application/json)

This endpoint expects a PromptVersionEnvironmentUpdate.

- `environments` (list of string, required)

## Response

### 204

No Content

## Errors

### 400 Bad Request Error

Bad Request

- `code` (integer, optional)
- `message` (string, optional)
- `details` (string, optional)

### 404 Not Found Error

Not Found

- `code` (integer, optional)
- `message` (string, optional)
- `details` (string, optional)

## Examples

**Request**

```json
{
  "environments": [
    "string"
  ]
}
```

**SDK Code**

```python
import requests

url = "http://localhost:5173/api/v1/private/prompts/versions/versionId/environments"

payload = { "environments": ["string"] }
headers = {"Content-Type": "application/json"}

response = requests.patch(url, json=payload, headers=headers)

print(response.json())
```

```javascript
const url = 'http://localhost:5173/api/v1/private/prompts/versions/versionId/environments';
const options = {
  method: 'PATCH',
  headers: {'Content-Type': 'application/json'},
  body: '{"environments":["string"]}'
};

try {
  const response = await fetch(url, options);
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error(error);
}
```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "http://localhost:5173/api/v1/private/prompts/versions/versionId/environments"

	payload := strings.NewReader("{\n  \"environments\": [\n    \"string\"\n  ]\n}")

	req, _ := http.NewRequest("PATCH", url, payload)

	req.Header.Add("Content-Type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:5173/api/v1/private/prompts/versions/versionId/environments")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Patch.new(url)
request["Content-Type"] = 'application/json'
request.body = "{\n  \"environments\": [\n    \"string\"\n  ]\n}"

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.patch("http://localhost:5173/api/v1/private/prompts/versions/versionId/environments")
  .header("Content-Type", "application/json")
  .body("{\n  \"environments\": [\n    \"string\"\n  ]\n}")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('PATCH', 'http://localhost:5173/api/v1/private/prompts/versions/versionId/environments', [
  'body' => '{
  "environments": [
    "string"
  ]
}',
  'headers' => [
    'Content-Type' => 'application/json',
  ],
]);

echo $response->getBody();
```

```csharp
using RestSharp;

var client = new RestClient("http://localhost:5173/api/v1/private/prompts/versions/versionId/environments");
var request = new RestRequest(Method.PATCH);
request.AddHeader("Content-Type", "application/json");
request.AddParameter("application/json", "{\n  \"environments\": [\n    \"string\"\n  ]\n}", ParameterType.RequestBody);
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = ["Content-Type": "application/json"]
let parameters = ["environments": ["string"]] as [String : Any]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:5173/api/v1/private/prompts/versions/versionId/environments")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "PATCH"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```