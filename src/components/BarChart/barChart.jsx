import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Bar } from '@ant-design/plots';

const BarChart = (props) => {
  const [data, setData] = useState([])

  useEffect(() => {
    setData(props.accidentCountData)
  }, [props.accidentCountData])
  /* 
  const data = [
    {
      year: '1951 年',
      value: 38,
    },
    {
      year: '1952 年',
      value: 52,
    },
    {
      year: '1956 年',
      value: 61,
    },
    {
      year: '1957 年',
      value: 145,
    },
    {
      year: '1958 年',
      value: 48,
    },
  ];*/
  const config = {
    data,
    xField: 'value',
    yField: 'type',
    seriesField: 'type',
    legend: {
      position: 'top-left',
    },
  };
  return <Bar {...config} />;
};

export default BarChart;