/**
 * Zero-Ops Garage Sale Automation
 * Handles SMS notifications and Status Updates
 */

const GATE_CODE = "1234"; // Update this with your actual code
const TWILIO_SID = "YOUR_TWILIO_SID"; // Optional
const TWILIO_TOKEN = "YOUR_TWILIO_TOKEN"; // Optional
const FROM_NUMBER = "YOUR_TWILIO_NUMBER"; // Optional

function onEdit(e) {
  const range = e.range;
  const sheet = range.getSheet();
  const rowIndex = range.getRow();
  const colIndex = range.getColumn();
  
  // Assuming 'Status' is Column 3
  if (colIndex === 3) {
    const status = range.getValue();
    const itemName = sheet.getRange(rowIndex, 1).getValue();
    const buyerPhone = sheet.getRange(rowIndex, 9).getValue(); // Assuming Phone is Col 9
    
    if (status === "Pick-up Ready" && buyerPhone) {
      sendSMS(buyerPhone, `Zain here! Your ${itemName} is ready in the mailroom (9 E 4th St). Gate code: ${GATE_CODE}. See ya!`);
    }
  }
}

function sendSMS(to, body) {
  // Option A: Twilio (Most Reliable)
  if (TWILIO_SID !== "YOUR_TWILIO_SID") {
    const url = `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_SID}/Messages.json`;
    const payload = {
      "To": to,
      "Body": body,
      "From": FROM_NUMBER
    };
    const options = {
      "method": "post",
      "payload": payload,
      "headers": {
        "Authorization": "Basic " + Utilities.base64Encode(TWILIO_SID + ":" + TWILIO_TOKEN)
      }
    };
    UrlFetchApp.fetch(url, options);
  } else {
    // Option B: Free
    Logger.log("SMS Triggered for: " + to + " Content: " + body);
    GmailApp.sendEmail("zain_khan@me.com", "SMS ALERT: " + to, body);
  }
}

function formatAndOrganizeSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // 1. Freeze Header
  sheet.setFrozenRows(1);
  sheet.getRange("A1:M1").setFontWeight("bold").setBackground("#f3f4f6");
  
  // 2. Add Dropdown for Condition (Col C)
  const conditionRule = SpreadsheetApp.newDataValidation().requireValueInList(
    ["Brand New", "Brand New - No Box", "Used Once", "Used a Lot"], true
  ).build();
  sheet.getRange(2, 3, 100, 1).setDataValidation(conditionRule);

  // 3. Add Dropdown for Status (Col D)
  const statusRule = SpreadsheetApp.newDataValidation().requireValueInList(
    ["Available", "Sold", "Pick-up Ready"], true
  ).build();
  sheet.getRange(2, 4, 100, 1).setDataValidation(statusRule);

  // 4. Inject Images into Column M (13)
const imageUrls = {
  "https://hamiltonbeach.com/10-cup-food-processor-70730": "https://hamiltonbeach.com/media/hamilton_beach_social.jpg",
  "https://www.ikea.com/us/en/p/uppdatera-flatware-tray-light-bamboo-20491356/": "https://www.ikea.com/us/en/images/products/uppdatera-flatware-tray-light-bamboo__0968836_pe810562_s5.jpg",
  "https://www.ikea.com/us/en/p/visslaan-drawer-organizers-set-of-3-gray-20562117/": "https://www.ikea.com/us/en/images/products/visslaan-drawer-organizers-set-of-3-gray__1499227_pe1006532_s5.jpg",
  "https://www.ikea.com/us/en/p/fejka-artificial-potted-plant-indoor-outdoor-hanging-eucalyptus-00615249/": "https://www.ikea.com/us/en/images/products/fejka-artificial-potted-plant-indoor-outdoor-hanging-eucalyptus__0817871_pe774216_s5.jpg",
  "https://www.ikea.com/us/en/p/montera-cable-management-white-30147425/": "https://www.ikea.com/us/en/images/products/montera-cable-management-white__0088067_pe218108_s5.jpg",
  "https://www.ikea.com/us/en/p/noedmast-led-portable-lamp-battery-operated-white-black-50582576/#content": "https://www.ikea.com/us/en/images/products/noedmast-led-portable-lamp-battery-operated-white-black__1300301_pe937090_s5.jpg",
  "https://www.walmart.com/ip/Mainstays-3-Bag-Mesh-Rolling-Sorter-Laundry-Cart-Soft-Silver/687612057?wmlspartner=wlpa&selectedSellerId=0&wl13=576&adid=22222222297687612057_0000000000_22264615354&wl0=&wl1=x&wl2=c&wl3=&wl4=&wl5=9026555&wl6=&wl7=&wl8=&wl9=pla&wl10=8175035&wl11=local&wl12=687612057&veh=sem&gclsrc=aw.ds&gad_source=1&gad_campaignid=22264616125&gbraid=0AAAAADmfBIpnJ_W9-HZEXfp0Um9yq8DSc&gclid=CjwKCAjwhe3OBhABEiwA6392zNvyiki2aiGDhFhb9USJK2jhB4OromQmQTlYC9Br6rNhVQL4-I_54hoCV64QAvD_BwE": "https://i5.walmartimages.com/seo/Mainstays-Soft-Silver-3-Bag-Mesh-Rolling-Laundry-Sorter-Cart_dccaf6bf-ec48-47d4-9b18-9f2ecf970e19.6e0c5b5786f0596674d58bb67a075152.jpeg",
  "https://www.ikea.com/us/en/p/bolloesund-drawer-organizers-set-of-4-beige-20570886/": "https://www.ikea.com/us/en/images/products/bolloesund-drawer-organizers-set-of-4-beige__1218055_pe913132_s5.jpg",
  "https://www.ikea.com/us/en/p/visslaan-box-with-compartments-gray-00562104/": "https://www.ikea.com/us/en/images/products/visslaan-box-with-compartments-gray__1499232_pe1006528_s5.jpg",
  "https://www.ikea.com/us/en/p/visslaan-box-with-lid-set-of-5-gray-90554538/": "https://www.ikea.com/us/en/images/products/visslaan-box-with-lid-set-of-5-gray__1499230_pe1006529_s5.jpg",
  "https://www.athome.com/potted-areca-palm-plant-6/124351622.html": "https://static.athome.com/images/w_800,h_800,c_pad,f_auto,fl_lossy,q_auto/v1734355251/p/124351622/potted-areca-palm-plant-6.jpg",
};
  
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  const links = sheet.getRange(2, 8, lastRow - 1, 1).getValues(); // Col H
  
  // Set header for Images
  sheet.getRange(1, 13).setValue("Reference Image").setFontWeight("bold").setBackground("#dcfce7");
  sheet.setColumnWidth(13, 120);

  for (let i = 0; i < links.length; i++) {
    const link = links[i][0];
    if (imageUrls[link]) {
      sheet.getRange(i + 2, 13).setFormula(`=IMAGE("${imageUrls[link]}", 4, 100, 100)`);
      sheet.setRowHeight(i + 2, 110);
    }
  }
}
