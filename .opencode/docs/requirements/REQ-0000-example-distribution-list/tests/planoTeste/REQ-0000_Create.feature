Feature: Distribution List endpoint URLs
  As an API client
  I want correct routing
  So that I can manage lists

  Scenario: Create routes to POST /lists
    When I POST to /lists
    Then the response status is 201

  Scenario: Retrieve routes to GET /lists/{id}
    When I GET /lists/1
    Then the response status is 200
