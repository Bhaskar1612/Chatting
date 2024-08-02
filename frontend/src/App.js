import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'
import Home from './Components/Home';
import SignIn from './Components/SignIn';
import SignUp from './Components/SignUp';
import Chat from './Components/Chat';


function App() {
  return (
    <div className="background-container">
    <Router>
      <Routes >
      <Route path='/' element={<Home/>} />
      <Route path='/signin' element={<SignIn/>} />
      <Route path='/signup' element={<SignUp/>} />
      <Route path='/chat' element={<Chat/>}/>
    </Routes>  
    </Router>
    </div>
  );
}

export default App;