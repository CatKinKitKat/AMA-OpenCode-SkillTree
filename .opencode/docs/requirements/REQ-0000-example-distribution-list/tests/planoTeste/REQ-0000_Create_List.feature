Feature: Distribution List create
  As an the-project operator
  I want to create a list
  So that alerts reach recipients

  Scenario: Happy path
    When I create a list "ops-alerts" with recipient "ops@example.com"
    Then the list exists with that recipient
