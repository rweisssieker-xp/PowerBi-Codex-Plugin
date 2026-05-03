import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const ROOT = path.resolve(".");
const OUTPUT_DIR = path.join(ROOT, "outputs", "powerbi-industrial-demo");
const OUTPUT_FILE = path.join(OUTPUT_DIR, "powerbi_industrial_demo_data.xlsx");

let seed = 424242;
function rand() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 4294967296;
}
function pick(items) {
  return items[Math.floor(rand() * items.length)];
}
function int(min, max) {
  return Math.floor(rand() * (max - min + 1)) + min;
}
function money(min, max) {
  return Number((min + rand() * (max - min)).toFixed(2));
}
function dateFrom(start, days) {
  const d = new Date(start);
  d.setDate(d.getDate() + int(0, days));
  return d;
}
function addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}
function iso(date) {
  return date.toISOString().slice(0, 10);
}
function col(n) {
  let s = "";
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - m) / 26);
  }
  return s;
}
function rowsToMatrix(rows) {
  const headers = Object.keys(rows[0] ?? { Empty: "" });
  return [headers, ...rows.map((row) => headers.map((h) => row[h] ?? null))];
}
function safeSheetName(name) {
  return name.slice(0, 31).replace(/[\\/?*[\]:]/g, "_");
}
const renderedSheets = [];
function writeSheet(workbook, name, rows) {
  const sheetName = safeSheetName(name);
  const sheet = workbook.worksheets.add(sheetName);
  renderedSheets.push(sheetName);
  const matrix = rowsToMatrix(rows.length ? rows : [{ Empty: "" }]);
  const range = sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);
  range.values = matrix;
  return sheet;
}

const companies = [
  { CompanyCode: "1000", CompanyName: "NordWerk Manufacturing GmbH", Currency: "EUR", Region: "EMEA" },
  { CompanyCode: "2000", CompanyName: "Atlantic Components Inc.", Currency: "USD", Region: "AMER" },
  { CompanyCode: "3000", CompanyName: "Asia Precision Pte Ltd", Currency: "SGD", Region: "APAC" },
];
const plants = [
  { PlantID: "DE10", CompanyCode: "1000", PlantName: "Hamburg Assembly", Country: "DE", Timezone: "Europe/Berlin", IndustryFocus: "Machinery" },
  { PlantID: "DE20", CompanyCode: "1000", PlantName: "Stuttgart Components", Country: "DE", Timezone: "Europe/Berlin", IndustryFocus: "Automotive" },
  { PlantID: "US10", CompanyCode: "2000", PlantName: "Ohio Fabrication", Country: "US", Timezone: "America/New_York", IndustryFocus: "Industrial Equipment" },
  { PlantID: "SG10", CompanyCode: "3000", PlantName: "Singapore Electronics", Country: "SG", Timezone: "Asia/Singapore", IndustryFocus: "Electronics" },
];
const warehouses = plants.flatMap((p) => [
  { WarehouseID: `${p.PlantID}-RAW`, PlantID: p.PlantID, WarehouseType: "RAW", WarehouseName: `${p.PlantName} Raw Materials` },
  { WarehouseID: `${p.PlantID}-FG`, PlantID: p.PlantID, WarehouseType: "FG", WarehouseName: `${p.PlantName} Finished Goods` },
  { WarehouseID: `${p.PlantID}-QI`, PlantID: p.PlantID, WarehouseType: "QUALITY", WarehouseName: `${p.PlantName} Quality Hold` },
]);

const segments = ["OEM", "Distributor", "Aftermarket", "Strategic Account", "Public Sector"];
const industries = ["Machinery", "Automotive", "Chemicals", "Electronics", "Aerospace", "Food", "Pharma"];
const countries = ["DE", "US", "FR", "NL", "IT", "CN", "SG", "PL", "ES", "GB"];
const customers = Array.from({ length: 60 }, (_, i) => ({
  CustomerID: `C${String(i + 1).padStart(4, "0")}`,
  CustomerName: `${pick(["Apex", "Global", "Prime", "Nova", "Atlas", "Vector", "Helio", "Orion"])} ${pick(["Industries", "Systems", "Mobility", "Components", "Technologies"])} ${i + 1}`,
  Segment: pick(segments),
  Industry: pick(industries),
  Country: pick(countries),
  SalesRegion: pick(["DACH", "Benelux", "North America", "Southern Europe", "APAC"]),
  CreditLimit: money(50000, 1500000),
  RiskClass: pick(["A", "B", "C", "Watch"]),
  ActiveFlag: rand() > 0.08,
}));

const productFamilies = ["Hydraulic Pump", "Control Cabinet", "Drive Unit", "Sensor Module", "Valve Block", "Service Kit", "Precision Motor"];
const products = Array.from({ length: 36 }, (_, i) => {
  const family = pick(productFamilies);
  return {
    ProductID: `P${String(i + 1).padStart(4, "0")}`,
    ProductName: `${family} ${pick(["Standard", "Plus", "Eco", "Pro", "Heavy Duty"])} ${100 + i}`,
    ProductFamily: family,
    ProductLine: pick(["Make-to-Stock", "Make-to-Order", "Engineer-to-Order", "Service"]),
    LifecycleStatus: pick(["Active", "Active", "Active", "Phase-out", "Launch"]),
    BaseUoM: "EA",
    StandardCost: money(120, 4200),
    ListPrice: money(250, 8800),
    WarrantyMonths: pick([12, 18, 24, 36]),
  };
});

const materials = Array.from({ length: 90 }, (_, i) => ({
  MaterialID: `M${String(i + 1).padStart(5, "0")}`,
  MaterialName: `${pick(["Casting", "Bearing", "PCB", "Seal", "Housing", "Cable", "Screw Set", "Motor", "Valve", "Sensor"])} ${i + 1}`,
  MaterialType: pick(["RAW", "HALB", "PACK", "SPARE"]),
  BaseUoM: pick(["EA", "KG", "M", "L"]),
  CommodityGroup: pick(["Metal", "Electronics", "Plastics", "Packaging", "Chemicals", "Services"]),
  StandardCost: money(1, 950),
  ShelfLifeDays: pick([0, 0, 180, 365, 730]),
  Criticality: pick(["Low", "Medium", "High", "Line Stopper"]),
}));

const suppliers = Array.from({ length: 35 }, (_, i) => ({
  SupplierID: `S${String(i + 1).padStart(4, "0")}`,
  SupplierName: `${pick(["Meyer", "Summit", "Pacific", "Euro", "Delta", "Zenith", "Kronos"])} ${pick(["Supply", "Metals", "Electronics", "Logistics", "Precision"])} ${i + 1}`,
  Country: pick(countries),
  SupplierType: pick(["Strategic", "Preferred", "Approved", "New", "Blocked"]),
  PaymentTerms: pick(["30D", "45D", "60D", "2%10Net30"]),
  ESGScore: int(45, 98),
  QualityRating: Number((85 + rand() * 14).toFixed(1)),
  OnTimeDeliveryPct: Number((75 + rand() * 24).toFixed(1)),
}));

const employees = Array.from({ length: 80 }, (_, i) => ({
  EmployeeID: `E${String(i + 1).padStart(4, "0")}`,
  EmployeeName: `${pick(["Anna", "Ben", "Clara", "David", "Eva", "Frank", "Grace", "Hiro", "Isabel", "Jon"])} ${pick(["Weber", "Miller", "Chen", "Garcia", "Khan", "Schmidt", "Brown", "Wang"])}`,
  Department: pick(["Sales", "Production", "Quality", "Maintenance", "Finance", "Supply Chain", "Warehouse", "Engineering"]),
  PlantID: pick(plants).PlantID,
  Role: pick(["Manager", "Planner", "Operator", "Engineer", "Controller", "Specialist"]),
  FTE: pick([1, 1, 1, 0.8, 0.5]),
}));

const workCenters = plants.flatMap((p, idx) =>
  Array.from({ length: 5 }, (_, i) => ({
    WorkCenterID: `WC-${p.PlantID}-${i + 1}`,
    PlantID: p.PlantID,
    WorkCenterName: `${pick(["Assembly", "Machining", "Testing", "Painting", "Packaging"])} Line ${i + 1}`,
    CapacityHoursPerDay: pick([8, 12, 16, 24]),
    CostRatePerHour: money(45, 160),
    BottleneckFlag: (idx + i) % 4 === 0,
  })),
);

const bom = products.flatMap((product) =>
  Array.from({ length: int(3, 7) }, (_, i) => {
    const material = pick(materials);
    return {
      ProductID: product.ProductID,
      BOMVersion: "V1",
      ComponentLine: i + 1,
      MaterialID: material.MaterialID,
      ComponentQty: Number((0.5 + rand() * 12).toFixed(3)),
      ComponentUoM: material.BaseUoM,
      ScrapPct: Number((rand() * 4).toFixed(2)),
      ValidFrom: "2025-01-01",
      ValidTo: "2099-12-31",
    };
  }),
);
const routings = products.flatMap((product) =>
  Array.from({ length: int(3, 5) }, (_, i) => {
    const wc = pick(workCenters);
    return {
      ProductID: product.ProductID,
      RoutingVersion: "R1",
      OperationNo: (i + 1) * 10,
      WorkCenterID: wc.WorkCenterID,
      SetupMinutes: int(10, 90),
      RunMinutesPerUnit: Number((2 + rand() * 35).toFixed(2)),
      QueueHours: Number((rand() * 16).toFixed(1)),
      QualityGateFlag: i === 1 || rand() > 0.75,
    };
  }),
);

const calendar = Array.from({ length: 730 }, (_, i) => {
  const d = new Date("2025-01-01T00:00:00Z");
  d.setUTCDate(d.getUTCDate() + i);
  const month = d.getUTCMonth() + 1;
  return {
    Date: iso(d),
    Year: d.getUTCFullYear(),
    Quarter: `Q${Math.floor((month - 1) / 3) + 1}`,
    MonthNo: month,
    MonthName: d.toLocaleString("en-US", { month: "short", timeZone: "UTC" }),
    FiscalYear: month >= 4 ? d.getUTCFullYear() : d.getUTCFullYear() - 1,
    FiscalPeriod: ((month + 8) % 12) + 1,
    IsWorkingDay: ![0, 6].includes(d.getUTCDay()),
  };
});

const leads = Array.from({ length: 160 }, (_, i) => {
  const created = dateFrom("2025-01-01T00:00:00Z", 480);
  return {
    LeadID: `L${String(i + 1).padStart(5, "0")}`,
    CreatedDate: iso(created),
    Source: pick(["Web", "Trade Fair", "Partner", "Outbound", "Existing Customer"]),
    Industry: pick(industries),
    Country: pick(countries),
    LeadScore: int(10, 100),
    Status: pick(["New", "Qualified", "Disqualified", "Converted"]),
    OwnerID: pick(employees.filter((e) => e.Department === "Sales")).EmployeeID,
  };
});
const opportunities = leads.filter(() => rand() > 0.25).map((lead, i) => {
  const customer = pick(customers);
  const created = addDays(new Date(`${lead.CreatedDate}T00:00:00Z`), int(1, 20));
  return {
    OpportunityID: `O${String(i + 1).padStart(5, "0")}`,
    LeadID: lead.LeadID,
    CustomerID: customer.CustomerID,
    CreatedDate: iso(created),
    Stage: pick(["Qualification", "Proposal", "Negotiation", "Won", "Lost"]),
    ProbabilityPct: int(10, 95),
    ExpectedValue: money(15000, 850000),
    ExpectedCloseDate: iso(addDays(created, int(15, 120))),
    SalesOwnerID: lead.OwnerID,
  };
});
const quotes = opportunities.filter(() => rand() > 0.18).map((opp, i) => {
  const created = addDays(new Date(`${opp.CreatedDate}T00:00:00Z`), int(2, 35));
  return {
    QuoteID: `Q${String(i + 1).padStart(5, "0")}`,
    OpportunityID: opp.OpportunityID,
    CustomerID: opp.CustomerID,
    QuoteDate: iso(created),
    QuoteStatus: pick(["Draft", "Submitted", "Approved", "Rejected", "Won"]),
    QuoteValue: money(10000, 700000),
    DiscountPct: Number((rand() * 18).toFixed(2)),
    ApprovalCycleDays: int(0, 21),
    LegalLoopCount: int(0, 4),
  };
});

const salesOrders = Array.from({ length: 260 }, (_, i) => {
  const q = pick(quotes);
  const orderDate = dateFrom("2025-02-01T00:00:00Z", 430);
  const product = pick(products);
  const qty = int(1, 80);
  const price = Number((product.ListPrice * (0.82 + rand() * 0.28)).toFixed(2));
  return {
    SalesOrderID: `SO${String(i + 1).padStart(6, "0")}`,
    QuoteID: q.QuoteID,
    CustomerID: q.CustomerID,
    ProductID: product.ProductID,
    PlantID: pick(plants).PlantID,
    OrderDate: iso(orderDate),
    RequestedDate: iso(addDays(orderDate, int(7, 60))),
    ConfirmedDate: iso(addDays(orderDate, int(10, 70))),
    OrderQty: qty,
    NetPrice: price,
    OrderValue: Number((qty * price).toFixed(2)),
    Status: pick(["Open", "Open", "Delivered", "Partially Delivered", "Cancelled"]),
    ATPStatus: pick(["Confirmed", "Shortage", "Partial", "Manual Review"]),
  };
});
const deliveries = salesOrders.filter(() => rand() > 0.14).map((so, i) => {
  const ship = addDays(new Date(`${so.OrderDate}T00:00:00Z`), int(8, 80));
  const deliveredQty = Math.max(1, Math.round(so.OrderQty * (0.75 + rand() * 0.25)));
  return {
    DeliveryID: `DLV${String(i + 1).padStart(6, "0")}`,
    SalesOrderID: so.SalesOrderID,
    CustomerID: so.CustomerID,
    ProductID: so.ProductID,
    WarehouseID: `${so.PlantID}-FG`,
    PickDate: iso(addDays(ship, -int(1, 4))),
    ShipDate: iso(ship),
    DeliveryDate: iso(addDays(ship, int(1, 12))),
    DeliveredQty: deliveredQty,
    OTIFStatus: new Date(ship) <= new Date(`${so.ConfirmedDate}T00:00:00Z`) && deliveredQty >= so.OrderQty ? "OTIF" : "Late/Short",
    Carrier: pick(["DHL", "DB Schenker", "Kuehne+Nagel", "UPS", "FedEx", "Maersk"]),
  };
});
const billings = deliveries.map((d, i) => {
  const so = salesOrders.find((x) => x.SalesOrderID === d.SalesOrderID);
  const invoiceDate = addDays(new Date(`${d.ShipDate}T00:00:00Z`), int(0, 7));
  return {
    InvoiceID: `INV${String(i + 1).padStart(6, "0")}`,
    DeliveryID: d.DeliveryID,
    SalesOrderID: d.SalesOrderID,
    CustomerID: d.CustomerID,
    InvoiceDate: iso(invoiceDate),
    DueDate: iso(addDays(invoiceDate, pick([30, 45, 60]))),
    InvoiceAmount: Number((d.DeliveredQty * so.NetPrice).toFixed(2)),
    TaxAmount: Number((d.DeliveredQty * so.NetPrice * 0.19).toFixed(2)),
    BillingBlockFlag: rand() > 0.92,
  };
});
const ar = billings.map((b) => {
  const paid = rand() > 0.22;
  return {
    InvoiceID: b.InvoiceID,
    CustomerID: b.CustomerID,
    DueDate: b.DueDate,
    OpenAmount: paid ? 0 : Number((b.InvoiceAmount * (0.2 + rand() * 0.8)).toFixed(2)),
    PaymentDate: paid ? iso(addDays(new Date(`${b.InvoiceDate}T00:00:00Z`), int(5, 75))) : null,
    DisputeFlag: !paid && rand() > 0.65,
    DunningLevel: paid ? 0 : int(0, 3),
  };
});

const purchaseReqs = Array.from({ length: 190 }, (_, i) => {
  const created = dateFrom("2025-01-01T00:00:00Z", 500);
  const mat = pick(materials);
  return {
    PurchaseReqID: `PR${String(i + 1).padStart(6, "0")}`,
    MaterialID: mat.MaterialID,
    PlantID: pick(plants).PlantID,
    RequestDate: iso(created),
    RequiredDate: iso(addDays(created, int(5, 75))),
    RequestedQty: int(10, 2500),
    RequesterID: pick(employees).EmployeeID,
    ApprovalStatus: pick(["Approved", "Approved", "Pending", "Rejected"]),
  };
});
const purchaseOrders = purchaseReqs.filter((pr) => pr.ApprovalStatus === "Approved").map((pr, i) => {
  const mat = materials.find((m) => m.MaterialID === pr.MaterialID);
  const orderDate = addDays(new Date(`${pr.RequestDate}T00:00:00Z`), int(1, 10));
  return {
    PurchaseOrderID: `PO${String(i + 1).padStart(6, "0")}`,
    PurchaseReqID: pr.PurchaseReqID,
    SupplierID: pick(suppliers).SupplierID,
    MaterialID: pr.MaterialID,
    PlantID: pr.PlantID,
    OrderDate: iso(orderDate),
    PromisedDate: iso(addDays(orderDate, int(7, 60))),
    OrderedQty: pr.RequestedQty,
    UnitPrice: Number((mat.StandardCost * (0.85 + rand() * 0.35)).toFixed(2)),
    POStatus: pick(["Open", "Open", "Received", "Partially Received", "Closed"]),
  };
});
const goodsReceipts = purchaseOrders.filter(() => rand() > 0.12).map((po, i) => {
  const received = Math.round(po.OrderedQty * (0.85 + rand() * 0.2));
  const receiptDate = addDays(new Date(`${po.OrderDate}T00:00:00Z`), int(5, 75));
  return {
    GoodsReceiptID: `GR${String(i + 1).padStart(6, "0")}`,
    PurchaseOrderID: po.PurchaseOrderID,
    SupplierID: po.SupplierID,
    MaterialID: po.MaterialID,
    WarehouseID: `${po.PlantID}-RAW`,
    ReceiptDate: iso(receiptDate),
    ReceivedQty: received,
    AcceptedQty: Math.round(received * (0.92 + rand() * 0.08)),
    InspectionLotID: rand() > 0.55 ? `QI${String(i + 1).padStart(6, "0")}` : null,
    DockToStockHours: Number((2 + rand() * 72).toFixed(1)),
  };
});
const ap = goodsReceipts.map((gr, i) => {
  const po = purchaseOrders.find((x) => x.PurchaseOrderID === gr.PurchaseOrderID);
  const invoiceDate = addDays(new Date(`${gr.ReceiptDate}T00:00:00Z`), int(0, 20));
  return {
    APInvoiceID: `AP${String(i + 1).padStart(6, "0")}`,
    PurchaseOrderID: gr.PurchaseOrderID,
    SupplierID: gr.SupplierID,
    InvoiceDate: iso(invoiceDate),
    DueDate: iso(addDays(invoiceDate, pick([30, 45, 60]))),
    InvoiceAmount: Number((gr.ReceivedQty * po.UnitPrice).toFixed(2)),
    GRIRDifference: money(-5000, 5000),
    BlockedFlag: rand() > 0.88,
  };
});

const forecasts = products.flatMap((p) =>
  plants.map((plant) =>
    Array.from({ length: 12 }, (_, m) => ({
      ForecastID: `FC-${p.ProductID}-${plant.PlantID}-${String(m + 1).padStart(2, "0")}`,
      ProductID: p.ProductID,
      PlantID: plant.PlantID,
      ForecastMonth: `2026-${String(m + 1).padStart(2, "0")}-01`,
      ForecastQty: int(20, 380),
      ConsensusQty: int(20, 380),
      ForecastVersion: "SOP-2026",
    })),
  ).flat(),
).flat();
const productionOrders = Array.from({ length: 220 }, (_, i) => {
  const p = pick(products);
  const start = dateFrom("2025-02-01T00:00:00Z", 430);
  const qty = int(5, 180);
  return {
    ProductionOrderID: `MO${String(i + 1).padStart(6, "0")}`,
    ProductID: p.ProductID,
    PlantID: pick(plants).PlantID,
    PlannedStart: iso(start),
    PlannedFinish: iso(addDays(start, int(1, 12))),
    ReleasedDate: iso(addDays(start, -int(0, 5))),
    OrderQty: qty,
    ConfirmedQty: Math.round(qty * (0.85 + rand() * 0.2)),
    ScrapQty: int(0, Math.max(1, Math.round(qty * 0.08))),
    OrderStatus: pick(["Created", "Released", "In Process", "Technically Complete", "Closed"]),
  };
});
const confirmations = productionOrders.flatMap((mo) =>
  routings
    .filter((r) => r.ProductID === mo.ProductID)
    .slice(0, int(2, 4))
    .map((r) => {
      const actualHours = Number(((r.SetupMinutes / 60) + (r.RunMinutesPerUnit * mo.ConfirmedQty) / 60) * (0.85 + rand() * 0.45)).toFixed(2);
      return {
        ConfirmationID: `CNF-${mo.ProductionOrderID}-${r.OperationNo}`,
        ProductionOrderID: mo.ProductionOrderID,
        ProductID: mo.ProductID,
        WorkCenterID: r.WorkCenterID,
        OperationNo: r.OperationNo,
        ConfirmationDate: iso(addDays(new Date(`${mo.PlannedStart}T00:00:00Z`), int(0, 12))),
        GoodQty: Math.max(0, mo.ConfirmedQty - int(0, mo.ScrapQty + 2)),
        ScrapQty: int(0, mo.ScrapQty + 2),
        ActualHours: actualHours,
        DowntimeMinutes: int(0, 180),
      };
    }),
);

const inventorySnapshot = materials.slice(0, 75).flatMap((m) =>
  warehouses.slice(0, 8).map((w) => {
    const qty = int(0, 12000);
    return {
      SnapshotDate: "2026-04-30",
      MaterialID: m.MaterialID,
      WarehouseID: w.WarehouseID,
      StockQty: qty,
      StockValue: Number((qty * m.StandardCost).toFixed(2)),
      SafetyStockQty: int(50, 900),
      BlockedQty: int(0, Math.round(qty * 0.08)),
      BatchManagedFlag: rand() > 0.55,
    };
  }),
);
const inventoryMovements = Array.from({ length: 500 }, (_, i) => {
  const m = pick(materials);
  const qty = int(1, 800);
  return {
    MovementID: `MV${String(i + 1).padStart(7, "0")}`,
    MovementDate: iso(dateFrom("2025-01-01T00:00:00Z", 515)),
    MaterialID: m.MaterialID,
    WarehouseID: pick(warehouses).WarehouseID,
    MovementType: pick(["101 Goods Receipt", "261 Consumption", "601 Delivery", "311 Transfer", "551 Scrap", "701 Inventory Adj."]),
    Quantity: qty,
    Amount: Number((qty * m.StandardCost * pick([1, 1, 1, -1])).toFixed(2)),
    ReferenceDoc: pick([...purchaseOrders.map((x) => x.PurchaseOrderID), ...productionOrders.map((x) => x.ProductionOrderID), ...salesOrders.map((x) => x.SalesOrderID)]),
  };
});

const inspections = goodsReceipts.filter((gr) => gr.InspectionLotID).map((gr) => ({
  InspectionLotID: gr.InspectionLotID,
  MaterialID: gr.MaterialID,
  SupplierID: gr.SupplierID,
  PlantID: gr.WarehouseID.slice(0, 4),
  LotCreatedDate: gr.ReceiptDate,
  InspectionEndDate: iso(addDays(new Date(`${gr.ReceiptDate}T00:00:00Z`), int(0, 10))),
  SampleQty: int(3, 50),
  DefectQty: int(0, 9),
  UsageDecision: pick(["Accepted", "Accepted", "Accepted", "Rejected", "Rework"]),
}));
const nonconformance = inspections.filter(() => rand() > 0.65).map((qi, i) => ({
  NCRID: `NCR${String(i + 1).padStart(5, "0")}`,
  InspectionLotID: qi.InspectionLotID,
  MaterialID: qi.MaterialID,
  SupplierID: qi.SupplierID,
  OpenDate: qi.InspectionEndDate,
  DefectType: pick(["Dimension", "Surface", "Documentation", "Functional", "Packaging", "Contamination"]),
  Severity: pick(["Minor", "Major", "Critical"]),
  Disposition: pick(["Use-as-is", "Rework", "Return to Supplier", "Scrap", "Pending"]),
  CostOfPoorQuality: money(250, 35000),
}));
const capa = nonconformance.map((ncr, i) => ({
  CAPAID: `CAPA${String(i + 1).padStart(5, "0")}`,
  NCRID: ncr.NCRID,
  OpenDate: ncr.OpenDate,
  DueDate: iso(addDays(new Date(`${ncr.OpenDate}T00:00:00Z`), int(14, 90))),
  OwnerID: pick(employees.filter((e) => e.Department === "Quality")).EmployeeID,
  RootCauseCategory: pick(["Supplier Process", "Machine Setup", "Operator Training", "Design", "Material Batch", "Transport"]),
  Status: pick(["Open", "In Progress", "Effectiveness Check", "Closed", "Overdue"]),
  EffectivenessPassedFlag: rand() > 0.28,
}));

const maintenanceOrders = Array.from({ length: 130 }, (_, i) => {
  const wc = pick(workCenters);
  const start = dateFrom("2025-01-01T00:00:00Z", 500);
  return {
    MaintenanceOrderID: `PM${String(i + 1).padStart(6, "0")}`,
    AssetID: `ASSET-${wc.WorkCenterID}`,
    WorkCenterID: wc.WorkCenterID,
    PlantID: wc.PlantID,
    OrderType: pick(["Preventive", "Corrective", "Inspection", "Calibration"]),
    Priority: pick(["Low", "Medium", "High", "Critical"]),
    CreatedDate: iso(start),
    CompletedDate: rand() > 0.18 ? iso(addDays(start, int(1, 20))) : null,
    DowntimeHours: Number((rand() * 28).toFixed(1)),
    MaintenanceCost: money(180, 48000),
    Status: pick(["Open", "Released", "Completed", "Closed", "Deferred"]),
  };
});
const serviceTickets = Array.from({ length: 150 }, (_, i) => {
  const opened = dateFrom("2025-01-01T00:00:00Z", 500);
  return {
    ServiceTicketID: `ST${String(i + 1).padStart(6, "0")}`,
    CustomerID: pick(customers).CustomerID,
    ProductID: pick(products).ProductID,
    InstalledBaseID: `IB${String(int(1, 500)).padStart(5, "0")}`,
    OpenDate: iso(opened),
    CloseDate: rand() > 0.22 ? iso(addDays(opened, int(1, 35))) : null,
    Priority: pick(["Low", "Medium", "High", "Critical"]),
    SLAStatus: pick(["Met", "Met", "At Risk", "Breached"]),
    WarrantyFlag: rand() > 0.45,
    ServiceCost: money(80, 22000),
  };
});
const shipments = deliveries.map((d) => ({
  ShipmentID: `SHP-${d.DeliveryID}`,
  DeliveryID: d.DeliveryID,
  Carrier: d.Carrier,
  Mode: pick(["Road", "Air", "Ocean", "Rail"]),
  PlannedPickup: d.PickDate,
  ActualPickup: iso(addDays(new Date(`${d.PickDate}T00:00:00Z`), int(-1, 2))),
  PlannedDelivery: d.DeliveryDate,
  ActualDelivery: iso(addDays(new Date(`${d.DeliveryDate}T00:00:00Z`), int(-2, 5))),
  FreightCost: money(120, 8500),
  CO2eKg: Number((30 + rand() * 3500).toFixed(1)),
}));
const glPostings = Array.from({ length: 600 }, (_, i) => {
  const amount = money(100, 250000) * pick([1, 1, 1, -1]);
  return {
    GLDocumentID: `GL${String(i + 1).padStart(7, "0")}`,
    CompanyCode: pick(companies).CompanyCode,
    PostingDate: iso(dateFrom("2025-01-01T00:00:00Z", 515)),
    FiscalYear: pick([2025, 2026]),
    GLAccount: pick(["400000 Revenue", "500000 COGS", "600000 Freight", "610000 Quality Cost", "700000 Opex", "120000 AR", "200000 AP"]),
    CostCenter: `CC-${int(100, 999)}`,
    ProfitCenter: `PC-${pick(plants).PlantID}`,
    Amount: Number(amount.toFixed(2)),
    Currency: "EUR",
    SourceProcess: pick(["O2C", "P2P", "Plan2Produce", "Quality", "Maintenance", "Service"]),
  };
});
const ehsIncidents = Array.from({ length: 55 }, (_, i) => {
  const incident = dateFrom("2025-01-01T00:00:00Z", 515);
  return {
    IncidentID: `EHS${String(i + 1).padStart(5, "0")}`,
    PlantID: pick(plants).PlantID,
    IncidentDate: iso(incident),
    IncidentType: pick(["Near Miss", "First Aid", "Lost Time", "Environmental", "Property Damage"]),
    Severity: pick(["Low", "Medium", "High", "Critical"]),
    LostTimeHours: int(0, 80),
    CorrectiveActionDue: iso(addDays(incident, int(7, 60))),
    Status: pick(["Open", "In Progress", "Closed", "Overdue"]),
  };
});

const dictionary = [
  ["Dim_Calendar", "Calendar dimension for date intelligence, fiscal period, and working-day logic."],
  ["Dim_Company", "Legal entities and currencies."],
  ["Dim_Plant", "Manufacturing and distribution sites."],
  ["Dim_Warehouse", "WHS/WMS warehouse structures."],
  ["Dim_Customer", "Customer master for CRM and O2C analytics."],
  ["Dim_Product", "Finished goods and product hierarchy."],
  ["Dim_Material", "Material master for BOM, P2P, inventory, and production."],
  ["Dim_Supplier", "Supplier master with quality, delivery, and ESG attributes."],
  ["Dim_Employee", "Employee/owner dimension for workflow ownership."],
  ["Dim_WorkCenter", "MES/routing work centers and capacity."],
  ["BillOfMaterials", "Product-component structure for BOM explosion and material churn."],
  ["RoutingOperations", "Arbeitsplan operations by product and work center."],
  ["Fact_Leads", "Market2Lead source data."],
  ["Fact_Opportunities", "Lead2Order opportunity pipeline."],
  ["Fact_Quotes", "Quote2Contract quote and approval data."],
  ["Fact_SalesOrders", "Order intake, ATP, backlog, order value."],
  ["Fact_Deliveries", "Pick, ship, delivery, OTIF."],
  ["Fact_Billing", "Billing, invoice, tax, billing block."],
  ["Fact_AR", "Receivables, disputes, dunning."],
  ["Fact_PurchaseReq", "Purchase requisitions and approvals."],
  ["Fact_PurchaseOrders", "Supplier orders, promised dates, prices."],
  ["Fact_GoodsReceipts", "Dock2Stock and receiving quality input."],
  ["Fact_AP", "AP invoices, GR/IR differences, blocks."],
  ["Fact_Forecast", "Demand planning and S&OP inputs."],
  ["Fact_ProductionOrders", "Plan2Produce/MES production order facts."],
  ["Fact_ProdConfirmations", "Shopfloor confirmations, scrap, downtime, OEE drivers."],
  ["Fact_InventorySnapshot", "Stock, value, blocked stock, safety stock."],
  ["Fact_InventoryMovements", "Material movements, scrap, transfers, consumption."],
  ["Fact_QualityInspections", "Inspection lots, samples, usage decisions."],
  ["Fact_Nonconformance", "NCR defects, severity, disposition, COPQ."],
  ["Fact_CAPA", "Corrective/preventive actions and effectiveness checks."],
  ["Fact_MaintenanceOrders", "EAM/CMMS reliability, downtime, maintenance cost."],
  ["Fact_ServiceTickets", "Aftermarket/service SLA and warranty cost."],
  ["Fact_Shipments", "TMS/logistics visibility, freight cost, CO2e."],
  ["Fact_GL_Postings", "FiCO/Record2Report financial postings by process."],
  ["Fact_EHS_Incidents", "EHS incident and action tracking."],
].map(([TableName, Purpose]) => ({ TableName, Purpose, Grain: "One row per business object or event as named", PowerBIUse: "Relate dimensions to facts by ID columns and build process-chain KPIs." }));

const readme = [
  {
    Workbook: "Power BI Industrial Demo Data",
    Description: "Synthetic demo workbook for testing Power BI process analytics across industrial enterprise sources.",
    DataPrivacy: "No real customer data. Deterministic generated data.",
    MainProcesses: "Market2Lead, Lead2Order, Quote2Contract, Order2Cash, Procure2Pay, Plan2Produce, Dock2Stock, Quality/CAPA, Maintain2Operate, Service, Record2Report, EHS/ESG.",
    Usage: "Load sheets into Power BI, create relationships on ID columns, then test semantic models, DAX, report layouts, AI/KI skills, and quality gates.",
  },
];

const workbook = Workbook.create();
writeSheet(workbook, "README", readme);
writeSheet(workbook, "Data_Dictionary", dictionary);
writeSheet(workbook, "Dim_Calendar", calendar);
writeSheet(workbook, "Dim_Company", companies);
writeSheet(workbook, "Dim_Plant", plants);
writeSheet(workbook, "Dim_Warehouse", warehouses);
writeSheet(workbook, "Dim_Customer", customers);
writeSheet(workbook, "Dim_Product", products);
writeSheet(workbook, "Dim_Material", materials);
writeSheet(workbook, "Dim_Supplier", suppliers);
writeSheet(workbook, "Dim_Employee", employees);
writeSheet(workbook, "Dim_WorkCenter", workCenters);
writeSheet(workbook, "BillOfMaterials", bom);
writeSheet(workbook, "RoutingOperations", routings);
writeSheet(workbook, "Fact_Leads", leads);
writeSheet(workbook, "Fact_Opportunities", opportunities);
writeSheet(workbook, "Fact_Quotes", quotes);
writeSheet(workbook, "Fact_SalesOrders", salesOrders);
writeSheet(workbook, "Fact_Deliveries", deliveries);
writeSheet(workbook, "Fact_Billing", billings);
writeSheet(workbook, "Fact_AR", ar);
writeSheet(workbook, "Fact_PurchaseReq", purchaseReqs);
writeSheet(workbook, "Fact_PurchaseOrders", purchaseOrders);
writeSheet(workbook, "Fact_GoodsReceipts", goodsReceipts);
writeSheet(workbook, "Fact_AP", ap);
writeSheet(workbook, "Fact_Forecast", forecasts);
writeSheet(workbook, "Fact_ProductionOrders", productionOrders);
writeSheet(workbook, "Fact_ProdConfirmations", confirmations);
writeSheet(workbook, "Fact_InventorySnapshot", inventorySnapshot);
writeSheet(workbook, "Fact_InventoryMovements", inventoryMovements);
writeSheet(workbook, "Fact_QualityInspections", inspections);
writeSheet(workbook, "Fact_Nonconformance", nonconformance);
writeSheet(workbook, "Fact_CAPA", capa);
writeSheet(workbook, "Fact_MaintenanceOrders", maintenanceOrders);
writeSheet(workbook, "Fact_ServiceTickets", serviceTickets);
writeSheet(workbook, "Fact_Shipments", shipments);
writeSheet(workbook, "Fact_GL_Postings", glPostings);
writeSheet(workbook, "Fact_EHS_Incidents", ehsIncidents);

const inspect = await workbook.inspect({
  kind: "table",
  range: "README!A1:E2",
  include: "values",
  tableMaxRows: 5,
  tableMaxCols: 8,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

await workbook.render({ sheetName: "README", range: "A1:E2", scale: 2 });
await workbook.render({ sheetName: "Data_Dictionary", range: "A1:D20", scale: 2 });
await workbook.render({ sheetName: "Fact_SalesOrders", range: "A1:M20", scale: 2 });
await workbook.render({ sheetName: "Fact_ProductionOrders", range: "A1:K20", scale: 2 });
for (const sheetName of renderedSheets) {
  await workbook.render({ sheetName, range: "A1:J12", scale: 1 });
}

await fs.mkdir(OUTPUT_DIR, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(OUTPUT_FILE);
console.log(`Saved ${OUTPUT_FILE}`);
