const express = require('express');
const router = express.Router();
const db = require('../db'); // Import the database connection

// Get all notices
router.get('/notices', async (req, res) => {
  try {
    const [results] = await db.query('SELECT * FROM notices');
    res.json(results);
  } catch (err) {
    res.status(500).json({ message: 'Error retrieving notices', error: err });
  }
});

// Get a specific notice by item_id
router.get('/notices/:item_id', async (req, res) => {
  const { item_id } = req.params;
  try {
    const [results] = await db.query('SELECT * FROM notices WHERE item_id = ?', [item_id]);
    if (results.length === 0) {
      res.status(404).json({ message: 'Notice not found' });
    } else {
      res.json(results[0]);
    }
  } catch (err) {
    res.status(500).json({ message: 'Error retrieving notice', error: err });
  }
});

module.exports = router;
