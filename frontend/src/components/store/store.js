import { configureStore, createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
    name: 'authorization',
    initialState: {
      isAuthorized: localStorage.getItem('token'),
    },
    reducers: {
      login: (state) => {
        state.isAuthorized  = true;
      },
      logout: (state) => {
        state.isAuthorized = false
      }
    },
});

const userProgress = createSlice({
  name: 'userProgress',
  initialState: {
    
  }
})

const store = configureStore({
  reducer: authSlice.reducer,
});

export const authActions = authSlice.actions;

export default store;

