
def palletsRec():
    palletsRecQuery = """SELECT * FROM
    ( SELECT CASE WHEN CustomerName >= 430 THEN 430 ELSE CustomerName END As ID,
    year(DeliveryDate) as year, IsNull(month(DeliveryDate), 0) as month,
    PalletsReceived FROM WarehouseReceipt WHERE DeliveryDate BETWEEN '1/01/2021 00:00:01' AND '07/31/2022 23:59:59' AND 
    CustomerName != 'PC' AND CustomerName != 'Z_TEST')  test
    PIVOT ( SUM(PalletsReceived) FOR month IN ([1] , [2] , [3] , [4] , [5] , [6] , [7] , [8] ,[9] , [10] , [11] , [12])) AS thingy ORDER BY ID, year desc"""
    return palletsRecQuery


def storageByUnit():
    storage = """
SELECT 
CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE CustomerName END As ID,
FORMAT(EffectiveDate, 'yyyyMM') AS YM,
TransactionType, Sum(QTY) As QTY
FROM InventoryTransaction
WHERE CustomerName = '425' AND FacilityName = 'Fullerton' AND TransactionType <4 
GROUP BY CustomerName ,  TransactionType, FORMAT(EffectiveDate, 'yyyyMM')
ORDER BY FORMAT(EffectiveDate, 'yyyyMM')
    """
    return storage


def inboundCharges():
    inbound = """
SELECT  DocumentInvoice.ReceiptNumber, 
WarehouseReceipt.DeliveryDate, WarehouseReceipt.CustomerOrderNumber,WarehouseReceipt.CustomerPONumber, 
WarehouseReceipt.CarrierName, WarehouseReceipt.TransportMethod, WarehouseReceipt.PalletsReceived, WarehouseReceipt.QtyReceived, WarehouseReceipt.LadingQuantity
"&InboundLinkList&"
FROM DocumentInvoice LEFT JOIN  DocumentInvoiceDetail ON DocumentInvoice.DocumentInvoiceNumber = DocumentInvoiceDetail.DocumentInvoiceNumber 
LEFT JOIN WarehouseReceipt ON DocumentInvoice.ReceiptNumber = WarehouseReceipt.ReceiptNumber AND DocumentInvoice.FacilityName = WarehouseReceipt.FacilityName

WHERE DocumentInvoice.CustomerName = "425" AND DocumentInvoice.InvoiceDate BETWEEN '6/1/2022' AND '6/30/2022' AND DocumentInvoice.FacilityName!='Ztest' AND DocumentInvoice.ReceiptNumber != 0
GROUP BY DocumentInvoice.CustomerName, DocumentInvoice.FacilityName, DocumentInvoice.ReceiptNumber, DocumentInvoice.InvoiceDate,
WarehouseReceipt.DeliveryDate, WarehouseReceipt.CustomerOrderNumber,WarehouseReceipt.CustomerPONumber,  WarehouseReceipt.CarrierName, WarehouseReceipt.TransportMethod, WarehouseReceipt.QtyReceived, WarehouseReceipt.LadingQuantity, WarehouseReceipt.PalletsReceived

ORDER BY DocumentInvoice.ReceiptNumber 
    """
    return inbound


def inAcc():
    inAcc = """
SELECT Accessorial.AccessorialName, Accessorial.AccessorialAlias, Accessorial.Description , AccessorialCriteria.TableName, AccessorialCriteria.FieldName, AccessorialCriteria.FieldValue,
AccessorialCriteria.ComparisonType, AccessorialCriteria.DataType

FROM Accessorial Left Join AccessorialCriteria ON Accessorial.AccessorialName = AccessorialCriteria.AccessorialName

WHERE Accessorial.GLCode = 'Inbound Handling' 
    """
    return inAcc


def inTar():
    inTar = """
SELECT Tariff.TariffName, Tariff.TariffAlias, Tariff.Description, TariffCriteria.TableName, TariffCriteria.FieldName, TariffCriteria.FieldValue, TariffCriteria.DataType

FROM Tariff Left Join TariffCriteria on Tariff.TariffName = TariffCriteria.TariffName

WHERE Tariff.GLCode = 'Inbound Handling'
    """
    return inTar


def unloadPalletized():
    unloadPallet = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.PalletsReceived*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.PalletsReceived*CustomerTariff.Rate) end  As CTN_CHarge 
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE  WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='UNLD PLTZD' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod = 'Palletized'
    """
    return unloadPallet


def lz1000():
    lz1000 = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND 
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE  WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='LZ<1000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized' AND WarehouseReceipt.LadingQuantity < 1000
    """
    return lz1000


def lz1T2T():
    lz1T2T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CNT_Charge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='LZ 1001-2000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity > 1000 AND WarehouseReceipt.LadingQuantity < 2001
    """
    return lz1T2T


def lz2T3T():
    lz2T3T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As UnloadPallets
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='LZ 2001-3000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity > 2000 AND WarehouseReceipt.LadingQuantity < 3001
    """
    return lz2T3T


def lz3T():
    lz3T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='LZ> 3000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity > 3000
    """
    return lz3T


def lz1T():
    lz1T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='LZ > 1000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity > 1000
    """
    return lz1T


def M2T():
    M2T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='FloorLoad Pieces:>2000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity >= 2000
    """
    return M2T

def Between1T2T():
    Between1T2T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='FloorLoad Pieces:1001-2000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity <= 2000 AND WarehouseReceipt.LadingQuantity >= 1000
    """
    return Between1T2T

def upTo1T():
    upTo1T = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='FloorLoad Up to: 1000' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.LadingQuantity <= 1000
    """
    return upTo1T


def UnldUnit():
    UnldUnit = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='UNLD UNIT' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'    
    """
    return UnldUnit


def UnldUnitAll():
    UnldUnitAll = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
Case When (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) < CustomerTariff.MinimumCharge Then CustomerTariff.MinimumCharge else (WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) end  As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='UNLD UNIT ALL' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM'    
    """
    return UnldUnitAll


def EAAway():
    EAAway = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='EA PUTAWAY' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM'    
    """
    return EAAway


def SrtConfirm():
    SrtConfirm = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerTariff.TariffName='SORT & CONFIRM' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.UniqueLotsReceived > 2   
    """
    return SrtConfirm


def SrtConfirm5():
    SrtConfirm5 = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerTariff.TariffName='SORT & CONFIRM 5+' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.UniqueLotsReceived > 4   
    """
    return SrtConfirm5


def SrtConfirmM():
    SrtConfirmM = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerTariff.TariffName='SORT & CONFIRM M' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod != 'Palletized'
AND WarehouseReceipt.UniqueLotsReceived > 4   
    """
    return SrtConfirmM


def InLabelCase():
    InLabelCase = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.LadingQuantity*CustomerTariff.Rate) As CTN_CHarge
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND CustomerTariff.TariffName='IN LABELING CS' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM'    
    """
    return InLabelCase


def palletPutaway():
    palletPutaway = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerTariff.TariffName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(WarehouseReceipt.PalletsReceived*CustomerTariff.Rate) As PalletPutaway
FROM WarehouseReceipt LEFT JOIN CustomerTariff ON WarehouseReceipt.CustomerName = CustomerTariff.CustomerName AND
WarehouseReceipt.FacilityName = CustomerTariff.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='402' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerTariff.TariffName='PLT PUTAWAY' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' 
    """
    return palletPutaway


def unload20():
    unload20 = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerAccessorial.AccessorialName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(CustomerAccessorial.Rate) As UnloadFlat
FROM WarehouseReceipt LEFT JOIN CustomerAccessorial ON WarehouseReceipt.CustomerName = CustomerAccessorial.CustomerName AND
WarehouseReceipt.FacilityName = CustomerAccessorial.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerAccessorial.AccessorialName='UNLD 20 FT FLR CNT' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod = '20 FLR'    
    """
    return unload20


def unload40():
    unload40 = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber) AS Thingy,CustomerAccessorial.AccessorialName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(CustomerAccessorial.Rate) As UnloadFlat
FROM WarehouseReceipt LEFT JOIN CustomerAccessorial ON WarehouseReceipt.CustomerName = CustomerAccessorial.CustomerName AND
WarehouseReceipt.FacilityName = CustomerAccessorial.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerAccessorial.AccessorialName='UNLD 40 FT FLR CNT' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod = '40 FLR'    
    """
    return unload40


def unload45():
    unload45 = """
SELECT CASE WHEN WarehouseReceipt.CustomerName >= 430 THEN 430 ELSE WarehouseReceipt.CustomerName END As ID,
Concat(WarehouseReceipt.CustomerName,WarehouseReceipt.FacilityName,WarehouseReceipt.ReceiptNumber)AS Thingy,CustomerAccessorial.AccessorialName,
Concat(Year(WarehouseReceipt.DeliveryDate),Month(WarehouseReceipt.DeliveryDate)) As Thingy2,
(CustomerAccessorial.Rate) As UnloadFlat
FROM WarehouseReceipt LEFT JOIN CustomerAccessorial ON WarehouseReceipt.CustomerName = CustomerAccessorial.CustomerName AND
WarehouseReceipt.FacilityName = CustomerAccessorial.FacilityName 
WHERE WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST' AND CustomerAccessorial.AccessorialName='UNLD 45 FT FLR CNT' AND
WarehouseReceipt.DeliveryDate BETWEEN '1/1/2022 12:00:00 AM' AND '7/31/2022 11:59:59 PM' AND WarehouseReceipt.TransportMethod = '45 FLR'    
    """
    return unload45


def AllInbound():
    allInbound = """
    SELECT
Concat(WarehouseReceipt.ReceiptNumber,WarehouseReceipt.FacilityName) AS Thingy, WarehouseReceipt.ReceiptNumber, WarehouseReceipt.DeliveryDate, WarehouseReceipt.FacilityName,
WarehouseReceipt.TransportMethod, WarehouseReceipt.QtyReceived, WarehouseReceipt.LadingQuantity, WarehouseReceipt.PalletsReceived
FROM WarehouseReceipt 
WHERE WarehouseReceipt.DeliveryDate BETWEEN '01/01/2022 00:00:01' AND '07/31/2022 23:59:59'
AND WarehouseReceipt.CustomerName != 'PC' AND WarehouseReceipt.CustomerName !='Z_TEST' AND WarehouseReceipt.FacilityName !='Z_TEST' AND WarehouseReceipt.FacilityName !='ZTEST'
    """
    return allInbound
