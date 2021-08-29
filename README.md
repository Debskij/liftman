[![codecov](https://codecov.io/gh/Debskij/liftman/branch/master/graph/badge.svg)](https://codecov.io/gh/Debskij/liftman)
[![Sanity check](https://github.com/Debskij/liftman/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Debskij/liftman/actions/workflows/main.yml)
# LIFTMAN
Project focused around creating solution for multiple elevators in single building

## Backstory
You are owner of modern, hotel where hotel residents can call elevator by using their phone.
With their smartphones they tell system where are they, and where they want to go. 
Elevator systems can use this knowledge to optimise route to give hotel residents best experience.

## Tasks 
* [x] Implement basic operations for one elevator
* [x] Implement basic operations for multiple elevators
* [x] Implement solution respecting passing by floors to optimise route for single elevator
* [x] Implement solution respecting passing by floors to optimise route for multiple elevators
* [x] Cover all functionalities with tests (without UI)
* [x] Create github actions workflow
* [x] Add test coverage badge
* [x] Add dockerfille
  
## Execution
Using python3.9 \
`python -m liftman`

Using docker \
`docker build -t liftman .`\
`docker run -it -t liftman`
