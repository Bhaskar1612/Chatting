import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignUp.css'; // Import your CSS file

const SignUp = () => {
  const navigate = useNavigate();
  const [memberDetails, setMemberDetails] = useState({
    username:'',
    password:''
  });



  const handleCreateMember = async () => {
    try {
      console.log(memberDetails);
      const response = await axios.post(`http://localhost:8000/signup/`, memberDetails);

      console.log('Member created:', response.data);
      alert('Registration Successful');
      navigate('/signin');
      // Handle success or navigate to a different page if needed
    } catch (error) {
      console.error('Error creating member:', error.response.data);
      alert('Enter a unique user');
      // Handle error, show an alert, etc.
    }
  };

  return (
    <div className="create-member-container">
      <h2>SignUp</h2>
      <div>
        <label>Username:</label>
        <input type="text" value={memberDetails.username} onChange={(e) => setMemberDetails({ ...memberDetails, username: e.target.value })} />
      </div>
      <div>
        <label>Password:</label>
        <input type="text" checked={memberDetails.password} onChange={(e) => setMemberDetails({ ...memberDetails, password: e.target.value })} />
      </div>
      <button onClick={handleCreateMember}>SignUp</button>
    </div>
  );
};

export default SignUp;