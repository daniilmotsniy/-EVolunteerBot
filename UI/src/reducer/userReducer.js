

const initialState = {user: null};

function userReducer(state, action) {
    switch (action.type) {
        case "setUser":
            let user = action.user || state.user;
            return {...state, user: user};
        default:
            throw Error("The action is not described");
    }
};

export {
    userReducer,
    initialState
};