import axios from 'axios';
import { useEffect, useState } from 'react';

function App() {
  const [notices, setNotices] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/notices')
      .then(response => setNotices(response.data))
      .catch(err => setError(err));
  }, []);

  return (
    <div>
      <h1>Notices</h1>
      {error && <p>Error loading notices: {error.message}</p>}
      <ul>
        {notices.map(notice => (
          <li key={notice.item_id}>{notice.item_title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
