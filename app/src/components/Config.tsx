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



function ConfigCommission() {
  const classes = useStyles();
  const [commission, setCommission] = React.useState(5);

  const handleCommissionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCommission(+event.target.value);
  };

  const handleSubmit = (event: FormEvent) => {
    const apiUrl = 'http://localhost:8200/api/config/commission';
    console.log(commission)
    const data = {'commission': commission}
    axios
      .patch(apiUrl, data)
      .then(function (response) { 
        if (response.status === 204) {
          alert("Succeed to configure the new commission")
        }
        
      })
      .catch(function (error) {
        alert(error);
      });
  };

  return (
    <form className={classes.root}>
      <TextField
        id="commission"
        label="commission"
        variant="filled"
        onChange={handleCommissionChange}
      />

      <Button onClick={handleSubmit} variant="contained">
        Config commission
      </Button>
    </form>
  );
}

export default ConfigCommission;
