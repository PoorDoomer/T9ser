# T9ser
This documentation includes details about each endpoint, the HTTP method, URL path, expected request body, and a brief description:

| Endpoint                       | HTTP Method | URL Path                                    | Description                                 | Example Request Body                                                                                     |
|--------------------------------|-------------|---------------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **List/Create Sports**         | GET, POST   | `/sports/`                                  | Retrieve all sports or create a new sport.  | POST: `{"name": "Soccer"}`                                                                                |
| **List/Create Matches**        | GET, POST   | `/matches/`                                 | Retrieve all matches or create a new match. | POST: `{"sport": 1, "host_user": 1, "location": "Local Stadium", "price": 20.00, "players_needed": 5, "date_time": "2023-07-20T18:00:00"}` |
| **Retrieve/Update/Delete Match** | GET, PUT, DELETE | `/matches/<int:pk>/`                   | Retrieve, update, or delete a specific match. | PUT: `{"location": "New Stadium", "price": 25.00}`                                                        |
| **List/Create User Matches**   | GET, POST   | `/usermatches/`                             | Retrieve all user matches or create a new one. | POST: `{"user": 2, "match": 1}`                                                                             |
| **Retrieve/Update/Delete User Match** | GET, PUT, DELETE | `/usermatches/<int:pk>/`             | Retrieve, update, or delete a specific user match. | None                                                                                                      |
| **List Match Participants**    | GET         | `/matches/<int:pk>/participants/`           | List all participants of a specific match. | None                                                                                                      |
| **Register User**              | POST        | `/register/`                                | Register a new user.                        | `{"username": "newuser", "email": "newuser@example.com", "password": "password123"}`                      |
| **Login User**                 | POST        | `/login/`                                   | Authenticate a user and retrieve a token.  | `{"username": "user", "password": "password123"}`                                                         |
| **Approve Participant**        | POST        | `/usermatches/approve/<int:pk>/`            | Approve a user's participation in a match. | None                                                                                                      |
| **User Profile**               | GET         | `/profile/`                                 | Retrieve the profile of the logged-in user. | None                                                                                                      |
| **My Matches**                 | GET         | `/my-matches/`                              | Retrieve matches the user is participating in. | None                                                                                                      |
| **Withdraw from Match**        | DELETE      | `/usermatches/withdraw/<int:pk>/`           | Withdraw from a match participation request. | None                                                                                                      |
| **Filtered Match List**        | GET         | `/matches/filter/`                          | Retrieve matches based on filters (sport, location, etc.). | None (use query parameters like `/matches/filter/?sport=1&location=stadium`)                            |

### Notes:

- Replace `<int:pk>` with the actual primary key (ID) of the relevant resource.
- The request bodies for `POST` and `PUT` methods are in JSON format.
- For endpoints requiring authentication (like creating matches, user matches, approving participants), the request must include an Authorization header with the user's token (e.g., `Authorization: Token <user_token>`).
- When filtering matches, query parameters can be appended to the URL (e.g., `/matches/filter/?sport=1`).

.
