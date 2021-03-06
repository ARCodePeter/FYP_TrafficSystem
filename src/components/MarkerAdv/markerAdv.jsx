import React from 'react'

const MarkerAdv = ({text}) => {
    return(
        <div style={{
            color: 'white',
            background: text === "left" ? "red" :  "yellow",
            padding: '7px 7px',
            display: 'inline-flex',
            textAlign: 'center',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '100%',
            transform: 'translate(-50%, -50%)',
            opacity: 0.7,
            fontSize: '10px',
        }}>
            
        </div>
    )
}

export default MarkerAdv;