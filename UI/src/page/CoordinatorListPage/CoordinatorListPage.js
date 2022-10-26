/**
 * Coordinator List page
 */

import React, { useContext, useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CircularProgress,
  Container,
  Grid,
  InputLabel,
  Select,
  MenuItem,
  Typography,
} from "@mui/material";

import { api, ORDER_STATUS } from "utils/api";
import { RowGrid } from "component";
import UserContext from "context/userContext";

const OrderConfirmedContext = React.createContext({
  updateCoordinatorList: () => {},
  statusSelected: ORDER_STATUS.NEW,
});

function OrderItem(props) {
  const {order} = props;
  const userContext = useContext(UserContext);
  const {user} = userContext;
  const orderConfirmedContext = useContext(OrderConfirmedContext);

  
  function updateOrderStatus(statusTo) {
    const orderId = order.order_id;
    api.updateOrderStatus(orderId, statusTo)
    .then(orderConfirmedContext.updateCoordinatorList);
  }

  function ButtonSet() {
    switch(orderConfirmedContext.statusSelected) {
      case ORDER_STATUS.NEW:
        return (
          <RowGrid >
            <Button
              color="success" variant="contained"
              onClick={() => (updateOrderStatus(ORDER_STATUS.APPROVED))}
            >Прийняти</Button>
          </RowGrid>
        );
      case ORDER_STATUS.APPROVED:
        return (
          <RowGrid>
            <Button
              color="warning" variant="contained"
              onClick={() => (updateOrderStatus(ORDER_STATUS.NEW))}
            >Відхилити</Button>
            <Button
              color="success" variant="contained"
              onClick={() => (updateOrderStatus(ORDER_STATUS.DELIVERED))}
            >Завершити</Button>
          </RowGrid>
        );
      case ORDER_STATUS.DELIVERED:
        return (user && user.roles.find(el => el === "admin")) ?
          (
            <RowGrid>
              <Button
                color="warning" variant="contained"
                onClick={() => (updateOrderStatus(ORDER_STATUS.APPROVED))}
              >Відхилити</Button>
              <Button
                color="info" variant="contained"
                onClick={() => { if (window.confirm('Ви впевнені що хочете архівувати замовлення?'))
                  (updateOrderStatus(ORDER_STATUS.ARCHIVED)) }}
              >Архівувати</Button>
            </RowGrid>
          ) : (
          <></>
        );
      default:
        throw new Error("The order status can not be handled");
      
    }
  }

  function FieldRow(props) {
    const { name, value } = props;
    return (
      <RowGrid insideKey={`${name}:${value}`}>
        <Typography color="text.secondary">{name}</Typography>
        <Typography fontWeight="500">{value}</Typography>
      </RowGrid>
    )
  }

  return (
    <Card>
      <Box maring={2}>
        
        <Container sx={{marginTop: "8px", marginBottom: "8px"}}>

          <RowGrid insideKey={0}>
            <Typography color="text.secondary" variant="h6">Замовленнe: </Typography>
            <Typography variant="h6">{order.order_id}</Typography>
          </RowGrid>
          {user && user.roles.find(el => el === "admin") && <FieldRow name="Оператор: " value={order.operator} />}
          
          <FieldRow name="Ім'я: " value={order.name} />
          <FieldRow name="Місто: " value={order.city} />
          <FieldRow name="Телефон: " value={order.phone} />
          <FieldRow name="Адреса: " value={order.address} />
          <FieldRow name="Людей: " value={order.people} />
          <FieldRow name="Можуть готувати: " value={order.can_cook ? 'Так' : 'Ні'} />
          <FieldRow name="Їжа: " value={order.food} />
          <FieldRow name="Медикаменти: " value={order.meds} />
          <FieldRow name="Коментар: " value={order.comment} />
          <FieldRow name="Дата: " value={order.date} />
        </Container>

        <Container>
          <Box my={2}>
            <ButtonSet />
          </Box>

          {/* <Button color="success" variant="contained" onClick={confirmOrder}>
            Прийняти
          </Button> */}
        </Container>

      </Box>
    </Card>
  )
}


function CoordinatorElement(props) {
  const {data} = props;
  return (
    <Card>
      <Box margin={2}>
          
        <RowGrid>
          <Typography color="text.secondary" variant="h6">Координатор: </Typography>
          <Typography variant="h6">{data.coordinators}</Typography>
        </RowGrid>
        {data.orders.map(order => (
          <OrderItem key={order.order_id} order={order} />
        ))}
      </Box>
    </Card>
  );
}

function CoordinatorListPage(props) {
  const [status, setStatus] = useState(ORDER_STATUS.NEW);
  const [coordinatorList, setCoordinatorList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [forcedUpdate, setForcedUpdate] = useState(new Date());

  const userContext = useContext(UserContext);
  const {user} = userContext;
  
  
  useEffect(() => {
    loadCoordinatorData(status)
    // .catch(error => {
    //   setLoading(false);
    //   setError("Error loading the data");
    // });
  }, [status, forcedUpdate]);

  function loadCoordinatorData() {
    setLoading(true);
    setError(null);
    api.getCooordinatorList(status)
    .then(({data}) => {
      setLoading(false);
      setError(false);
      setCoordinatorList(data);
    })
    .catch(err => {
      setError("Unknown error occured");
    })
  }

  function handleSelectStatus(e) {
    setStatus(e.target.value);
  }

  function downloadPDF(e) {
    e.preventDefault();
    api.getPDFReport()
    .then(response => {
      let pdfURL = response.data;
      // window.open(pdfURL, '_blank').focus();
      const link = document.createElement("a");
      link.href = pdfURL;
      link.download = "KharkivBayraktarReport.pdf";
      link.click();

    })
  }
  
  return (
    <>
    {/* Form bar container */}
    <Box sx={{my: 2}}>
      <Grid container alignItems={"flexEnd"}>

        <Grid item flexGrow={1}>
          <InputLabel id="status-select-label">Статус</InputLabel>
          <Select
            labelId="status-select-label"
            id="status-select"
            value={status}
            label="Статус"
            onChange={handleSelectStatus}
          >
            <MenuItem value={ORDER_STATUS.NEW}>Новий</MenuItem>
            <MenuItem value={ORDER_STATUS.APPROVED}>Зібраний</MenuItem>
            <MenuItem value={ORDER_STATUS.DELIVERED}>Доставлений</MenuItem>
          </Select>
        </Grid>
        {(user && user.roles.find(el => el === "admin")) ? (
          <Grid item alignSelf="center">
          <Button
            color="info" variant="contained"
            onClick={downloadPDF}
          >Download PDF</Button>
          </Grid>
        ) :
        (<></>)
        }

      </Grid>

    </Box>

      {error ?
        <Typography>{error}</Typography>
        :
        <>
          <Grid container direction="column">
            {
              loading ? 
                <Grid item>
                  <Box sx={{ display: 'flex' }}>
                    <CircularProgress />
                  </Box>
                </Grid>
              :
                coordinatorList.length ?
                  <OrderConfirmedContext.Provider value={{
                    updateCoordinatorList:() => setForcedUpdate(new Date()),
                    statusSelected: status,
                    }}>
                    {
                      coordinatorList.map(el => (
                      <Grid key={el.coordinator} item>
                        <CoordinatorElement data={el}/>
                      </Grid>
                    ))
                  }
                  </OrderConfirmedContext.Provider>
                :
                  <Typography variant="h4" color="GrayText">The list of coordinators is empty</Typography>
            }
          </Grid>
        </>
      }
    </>
  )
}

export default CoordinatorListPage;
