import { Button, MenuItem, TextField } from "@material-ui/core";
import { makeStyles, createStyles, Theme } from "@material-ui/core/styles";
import React, { FormEvent } from "react";
import axios from "axios";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      "& .MuiTextField-root": {
        margin: theme.spacing(1),
        width: "25ch",
      },
    },
  })
);

const currencies = [
  "AFN",
  "ALL",
  "DZD",
  "AOA",
  "ARS",
  "AMD",
  "AWG",
  "AUD",
  "AZN",
  "BSD",
  "BHD",
  "BBD",
  "BDT",
  "BYR",
  "BZD",
  "BMD",
  "BTN",
  "BTC",
  "BCH",
  "BOB",
  "BAM",
  "BWP",
  "BRL",
  "BND",
  "BGN",
  "BIF",
  "XPF",
  "KHR",
  "CAD",
  "CVE",
  "KYD",
  "XAF",
  "CLP",
  "CLF",
  "CNY",
  "CNH",
  "COP",
  "KMF",
  "CDF",
  "CRC",
  "HRK",
  "CUP",
  "CZK",
  "DKK",
  "DJF",
  "DOP",
  "XCD",
  "EGP",
  "ETH",
  "ETB",
  "EUR",
  "FJD",
  "GMD",
  "GEL",
  "GHC",
  "GIP",
  "GTQ",
  "GNF",
  "GYD",
  "HTG",
  "HNL",
  "HKD",
  "HUF",
  "ISK",
  "INR",
  "IDR",
  "IRR",
  "IQD",
  "ILS",
  "JMD",
  "JPY",
  "JOD",
  "KZT",
  "KES",
  "KWD",
  "KGS",
  "LAK",
  "LBP",
  "LSL",
  "LRD",
  "LYD",
  "LTC",
  "MOP",
  "MKD",
  "MGA",
  "MWK",
  "MYR",
  "MVR",
  "MRO",
  "MUR",
  "MXN",
  "MDL",
  "MAD",
  "MZM",
  "MMK",
  "TWD",
  "NAD",
  "NPR",
  "ANG",
  "NZD",
  "NIO",
  "NGN",
  "NOK",
  "OMR",
  "PKR",
  "PAB",
  "PGK",
  "PYG",
  "PHP",
  "PLN",
  "GBP",
  "QAR",
  "ROL",
  "RUR",
  "RUB",
  "RWF",
  "SVC",
  "SAR",
  "CSD",
  "SCR",
  "SLL",
  "SGD",
  "PEN",
  "SBD",
  "SOS",
  "ZAR",
  "KRW",
  "VEF",
  "XDR",
  "LKR",
  "SSP",
  "SRD",
  "SZL",
  "SEK",
  "CHF",
  "TJS",
  "TZS",
  "THB",
  "TOP",
  "TTD",
  "TND",
  "TRY",
  "TMM",
  "UGX",
  "UAH",
  "AED",
  "USD",
  "UYU",
  "UZS",
  "VND",
  "XOF",
  "YER",
  "ZMW",
];

function Exchange() {
  const classes = useStyles();
  const [currency, setCurrency] = React.useState("USD");
  const [targetCurrency, setTargetCurrency] = React.useState("EUR");
  const [amount, setAmount] = React.useState(0);

  const handleAmountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAmount(+event.target.value);
  };

  const handleCurrencyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCurrency(event.target.value);
  };

  const handleTargetCurrencyChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setTargetCurrency(event.target.value);
  };

  const handleSubmit = (event: FormEvent) => {
    const apiUrl = `http://localhost:8200/api/exchange?amount=${amount}&originCurrency=${currency}&targetCurrency=${targetCurrency}`;
    axios
      .get(apiUrl)
      .then(function (response) {
          
        alert(response.data)
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <form className={classes.root}>
      <TextField
        id="amount"
        label="amount"
        variant="filled"
        onChange={handleAmountChange}
      />
      <TextField
        id="currency"
        select
        label="Currency"
        value={currency}
        onChange={handleCurrencyChange}
        helperText="Select currency"
      >
        {currencies.map((currency) => (
          <MenuItem key={currency} value={currency}>
            {currency}
          </MenuItem>
        ))}
      </TextField>
      <TextField
        id="currency"
        select
        label="Target Currency"
        value={targetCurrency}
        onChange={handleTargetCurrencyChange}
        helperText="Select Target Currency"
      >
        {currencies.map((targetCurrency) => (
          <MenuItem key={targetCurrency} value={targetCurrency}>
            {targetCurrency}
          </MenuItem>
        ))}
      </TextField>
      <Button onClick={handleSubmit} variant="contained">
        Exchange money
      </Button>
    </form>
  );
}

export default Exchange;
