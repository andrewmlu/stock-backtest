import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2'
import Chart from 'chart.js/auto';
import zoomPlugin from 'chartjs-plugin-zoom';

function App() {
  const [query, setQuery] = useState({
    ticker:'', startdate:'', enddate:'', freq:'', init_amnt:'', rec_amnt:''
  })

  const [series, setSeries] = useState([])
  // useEffect(() => {
  //   console.log('HELLO');
  //   const { data } = axios.get('http://127.0.0.1:5000/AAPL/20210325/20210822/5/1/1').then(res => {
  //     console.log("SUCCESS", res);
  //     setQuery(res)
  //   });
  // }, [])  
  // console.log("NEWDATA", newdata);

  const [userData, setUserData] = useState({
    labels: [],
    datasets: []
  })

  const backtest_path = 'http://127.0.0.1:5000/'

  const handleSubmit = (e) => {
    e.preventDefault();
    const url = `${backtest_path}${query.ticker}/${query.startdate}/${query.enddate}/${query.freq}/${query.init_amnt}/${query.rec_amnt}`;
    axios.get(url).then(res => {
      console.log("SUCCESS", res);
      setSeries(res) ;
    });
  }

  useEffect(() => {
    setUserData(
      ('data' in series) ? 
      {
        labels: series.data.map((data) => data.date),
        datasets: [{
          label: "Total Value",
          data: series.data.map((data) => data.value),
          backgroundColor: ['green']
        },
        {
          label: "Stock Price",
          data: series.data.map((data) => data.close),
          backgroundColor: ['blue']
        },
        {
          label: "Total Investment",
          data: series.data.map((data) => data.invested),
          backgroundColor: ['orange']
        },
        {
          label: "Holdings",
          data: series.data.map((data) => data.holdings),
          backgroundColor: ['purple']
        }
        ]
      }
       : 
      { 
      labels: [],
      datasets: []
      }
    );
    console.log('TESTING', query);
    console.log('USER_DATA', userData);
  }, 

  [series]);

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <input class="form-text" placeholder='ticker' onChange={(e) => setQuery({...query, ticker: e.target.value})} />
        <input class="form-text" placeholder='start date (YYYYMMDD)' onChange={(e) => setQuery({...query, startdate: e.target.value})} />
        <input class="form-text" placeholder='end date (YYYYMMDD)' onChange={(e) => setQuery({...query, enddate: e.target.value})} />
        <input class="form-text" placeholder='initial investment' onChange={(e) => setQuery({...query, init_amnt: e.target.value})} />
        <input class="form-text" placeholder='recurring investment' onChange={(e) => setQuery({...query, rec_amnt: e.target.value})} />
        <input class="form-text" placeholder='frequency of recurring (days)' onChange={(e) => setQuery({...query, freq: e.target.value})} />
        <button>Click me</button>
      </form>
      { series.status === 200 ? <div class="graph" style={{width: 900}}>
        <Line data={userData} />
      </div>
      : ''}
    </div>

  );
}

export default App;
