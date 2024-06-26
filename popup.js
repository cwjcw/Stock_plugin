document.getElementById('getData').addEventListener('click', function() {
    let ticker = document.getElementById('ticker').value;
    fetchStockData(ticker);
  });
  
  function fetchStockData(ticker) {
    const url = `http://127.0.0.1:5000/stock/${ticker}`;  // 本地Flask服务器的URL
    
    fetch(url)
      .then(response => response.json())
      .then(data => {
        displayData(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('result').innerText = 'Error fetching data.';
      });
  }
  
  function displayData(data) {
    if (data.error) {
      document.getElementById('result').innerText = 'Error fetching data.';
    } else {
      document.getElementById('result').innerText = data.data;
    }
  }
  