# nerdery-snacks
Basic snack api/ui. Users can create accounts then suggest + vote on snacks. WIP.

### running the api + UI
Requirements:
  - docker and docker-compose
  - secret key for snacks api (insert into docker-compose.yml environment variables)

then run `make compose`. There is a race condition for the database / api that [wait_for_it.sh](api/wait_for_it.sh) should solve but it isn't consistent. If it fails to come up, simply run `make compose` again

Navigate to [http://localhost:3000/vote](http://localhost:3000/vote) to see the frontend

Note, the frontend could be static, but to lower the reqs for running I wrapped it into a docker container

### UI
The frontend is ugly but functional. UI components from [material-ui@next](https://material-ui-next.com/) were used to bootstrap the style, but I didn't put much time into the layout so they are all bunched together

#### How to use
When the services come up the db is blank.
- Create a user by clicking Log In in the upper right. Click the `New User` link
- Log in with your new username and password
- After login you are directed to the `Vote` page. Use this page to vote on any eligible snacks. There likely won't be any eligible snacks until you suggest a snack
- Head to the `Suggestion` page to suggest a snack for voting.
