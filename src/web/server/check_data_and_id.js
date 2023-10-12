const chech_data_and_id = (value) => {
    id = Math.floor(parseInt(value)%10);
    
    if (Math.floor(parseInt(value)/10) === 0) {
        displayValue = id + '非常に空いています';
    } else if (Math.floor(parseInt(value)/10) === 1) {
        displayValue = id + '空いています';
    } else if (Math.floor(parseInt(value)/10) === 2) {
        displayValue = id + '混雑しています';
    } else if (Math.floor(parseInt(value)/10) === 3) {
        displayValue = id + '非常に混雑しています';
    } else {
        displayValue = 'loading...';
    }

    return displayValue;
  }

  module.exports = chech_data_and_id;