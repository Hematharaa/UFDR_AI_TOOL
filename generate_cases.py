import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import hashlib

# Create cases directory
os.makedirs("case_files", exist_ok=True)

def generate_phone_forensics_case(case_id, num_records=200):
    """Generate mobile phone forensic data"""
    
    suspects = [
        {'name': 'Rajesh Kumar', 'phone': '+919876543210', 'city': 'Mumbai', 'country': 'India', 'crime': 'Cyber Fraud'},
        {'name': 'John Smith', 'phone': '+447890123456', 'city': 'London', 'country': 'UK', 'crime': 'Money Laundering'},
        {'name': 'Ahmed Khan', 'phone': '+971501234567', 'city': 'Dubai', 'country': 'UAE', 'crime': 'Crypto Fraud'},
        {'name': 'Michael Brown', 'phone': '+12025550123', 'city': 'New York', 'country': 'USA', 'crime': 'Identity Theft'},
        {'name': 'Li Wei', 'phone': '+86123456789', 'city': 'Beijing', 'country': 'China', 'crime': 'Phishing'},
        {'name': 'Priya Sharma', 'phone': '+919812345678', 'city': 'Delhi', 'country': 'India', 'crime': 'Bank Fraud'},
        {'name': 'David Lee', 'phone': '+61234567890', 'city': 'Sydney', 'country': 'Australia', 'crime': 'Drug Trafficking'},
        {'name': 'Maria Garcia', 'phone': '+34912345678', 'city': 'Madrid', 'country': 'Spain', 'crime': 'Extortion'},
        {'name': 'Yuki Tanaka', 'phone': '+81312345678', 'city': 'Tokyo', 'country': 'Japan', 'crime': 'Hacking'},
        {'name': 'Hans Mueller', 'phone': '+491512345678', 'city': 'Berlin', 'country': 'Germany', 'crime': 'Ransomware'},
        {'name': 'Sarah Wilson', 'phone': '+14165550123', 'city': 'Toronto', 'country': 'Canada', 'crime': 'Identity Fraud'},
        {'name': 'Ali Hassan', 'phone': '+966501234567', 'city': 'Riyadh', 'country': 'Saudi Arabia', 'crime': 'Terror Funding'},
        {'name': 'Olga Petrova', 'phone': '+74951234567', 'city': 'Moscow', 'country': 'Russia', 'crime': 'Ransomware'},
        {'name': 'Chen Wei', 'phone': '+88612345678', 'city': 'Taipei', 'country': 'Taiwan', 'crime': 'Hacking'},
        {'name': 'Carlos Lopez', 'phone': '+525512345678', 'city': 'Mexico City', 'country': 'Mexico', 'crime': 'Drug Cartel'}
    ]
    
    evidence_types = ['WhatsApp Chat', 'Telegram Chat', 'Signal Chat', 'SMS', 'Call Log', 
                      'Contact', 'Location', 'Browser History', 'App Data', 'Deleted File',
                      'Email', 'Document', 'Image', 'Video']
    
    crypto_keywords = ['BTC', 'bitcoin', 'wallet', 'crypto', 'blockchain', 'mining', 'exchange', 'private key', 'USDT', 'Ethereum']
    suspicious_keywords = ['delete', 'destroy', 'hide', 'encrypt', 'secret', 'midnight', 'urgent', 'kill', 'weapon', 'bomb', 'drugs']
    
    data = []
    
    for i in range(num_records):
        suspect = random.choice(suspects)
        evidence_type = random.choice(evidence_types)
        
        # Generate timestamp
        days_ago = random.randint(0, 90)
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours, minutes=minutes, seconds=seconds)
        
        # Generate content
        if 'Chat' in evidence_type:
            msg_type = random.choice(['normal', 'suspicious', 'crypto'])
            if msg_type == 'crypto':
                content = f"Send 2.5 BTC to wallet bc1q{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))}"
            elif msg_type == 'suspicious':
                content = f"Meet at {random.choice(['Airport', 'Hotel', 'Mall', 'Park', 'Warehouse'])} at {random.randint(20,23)}:00. Come alone."
            else:
                content = f"Normal conversation about {random.choice(['meeting', 'delivery', 'payment', 'documents', 'schedule'])}"
        
        elif evidence_type == 'Call Log':
            duration = random.randint(10, 3600)
            content = f"Call duration: {duration} seconds - {random.choice(['Incoming', 'Outgoing', 'Missed'])}"
        
        elif evidence_type == 'SMS':
            if random.random() > 0.5:
                content = f"OTP: {random.randint(100000, 999999)} for transaction of ${random.randint(1000, 99999)}"
            else:
                content = f"Your package will be delivered tomorrow. Tracking: TRK{random.randint(10000, 99999)}"
        
        elif evidence_type == 'Location':
            coords = f"{random.uniform(-90, 90):.6f}, {random.uniform(-180, 180):.6f}"
            content = f"GPS: {coords} - {random.choice(['Home', 'Office', 'Unknown', 'Foreign Location', 'Border Area'])}"
        
        elif evidence_type == 'Email':
            content = f"Subject: {random.choice(['URGENT', 'Confidential', 'Meeting', 'Report'])} - Please review the attached documents"
        
        else:
            content = f"File: evidence_{i}.{random.choice(['jpg', 'pdf', 'txt', 'mp4', 'docx'])}"
        
        # Calculate risk score
        risk_score = 0
        if any(word in content.lower() for word in crypto_keywords):
            risk_score += 40
        if any(word in content.lower() for word in suspicious_keywords):
            risk_score += 35
        if suspect['country'] not in ['India', 'China', 'Japan']:
            risk_score += 20
        if timestamp.hour in [22, 23, 0, 1, 2, 3, 4]:
            risk_score += 15
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = 'CRITICAL'
        elif risk_score >= 50:
            risk_level = 'HIGH'
        elif risk_score >= 30:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # File size for media
        file_size = random.randint(10, 50000) if evidence_type in ['Image', 'Video', 'Document'] else 0
        
        data.append({
            'Evidence ID': f"{case_id}-{str(i+1).zfill(6)}",
            'Case ID': case_id,
            'Suspect Name': suspect['name'],
            'Suspect Phone': suspect['phone'],
            'City': suspect['city'],
            'Country': suspect['country'],
            'Crime Type': suspect['crime'],
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Evidence Type': evidence_type,
            'Source App': random.choice(['WhatsApp', 'Telegram', 'Signal', 'Phone', 'SMS', 'Email', 'Gallery']),
            'Content': content[:250],
            'File Hash': hashlib.md5(content.encode()).hexdigest()[:16],
            'File Size (KB)': file_size,
            'Is Deleted': random.random() < 0.15,
            'Is Encrypted': random.random() < 0.10,
            'Risk Score': risk_score,
            'Risk Level': risk_level,
            'Flagged': risk_level in ['CRITICAL', 'HIGH'],
            'Investigator Notes': '',
            'Chain of Custody': f"Seized on {(datetime.now() - timedelta(days=random.randint(30, 60))).strftime('%Y-%m-%d')}",
            'Device Type': random.choice(['iPhone 15 Pro', 'Samsung S24 Ultra', 'Google Pixel 8', 'OnePlus 12', 'Xiaomi 14', 'iPad Pro']),
            'OS Version': random.choice(['iOS 17', 'Android 14', 'Windows 11', 'macOS Sonoma']),
            'Extraction Method': random.choice(['Physical', 'Logical', 'File System', 'Chip-off']),
            'Case Status': random.choice(['Active', 'Under Investigation', 'Closed', 'Court Ready'])
        })
    
    return pd.DataFrame(data)

# Generate 50 different case files
crime_types = ['Cyber Fraud', 'Money Laundering', 'Drug Trafficking', 'Terror Funding', 
               'Identity Theft', 'Ransomware', 'Phishing', 'Crypto Scam', 'Extortion', 
               'Hacking', 'Child Exploitation', 'Weapons Trafficking', 'Human Trafficking',
               'Bank Fraud', 'Insurance Fraud', 'Copyright Infringement', 'Cyber Stalking']

print("=" * 50)
print("🔍 GENERATING 50 FORENSIC CASE FILES")
print("=" * 50)

for i in range(1, 51):
    case_id = f"CX-2026-{str(i).zfill(3)}"
    crime_type = random.choice(crime_types)
    num_records = random.randint(150, 350)
    
    print(f"\n📁 Generating case {i}/50: {case_id}")
    print(f"   Crime Type: {crime_type}")
    print(f"   Records: {num_records}")
    
    df = generate_phone_forensics_case(case_id, num_records)
    
    # Save to CSV
    filename = f"case_files/UFDR_CASE_{case_id}_{crime_type.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    
    # Count risk levels
    critical = len(df[df['Risk Level'] == 'CRITICAL'])
    high = len(df[df['Risk Level'] == 'HIGH'])
    medium = len(df[df['Risk Level'] == 'MEDIUM'])
    low = len(df[df['Risk Level'] == 'LOW'])
    
    print(f"   ✅ Saved: {filename}")
    print(f"   📊 Risk Distribution: Critical:{critical} High:{high} Medium:{medium} Low:{low}")

print("\n" + "=" * 50)
print("🎉 SUCCESSFULLY GENERATED 50 CASE FILES!")
print("=" * 50)

# Create a summary file
print("\n📊 Creating summary report...")
summary = []
for filename in os.listdir("case_files"):
    if filename.endswith('.csv') and filename != 'cases_summary.csv':
        df = pd.read_csv(f"case_files/{filename}")
        summary.append({
            'Filename': filename,
            'Total Records': len(df),
            'Critical': len(df[df['Risk Level'] == 'CRITICAL']),
            'High': len(df[df['Risk Level'] == 'HIGH']),
            'Medium': len(df[df['Risk Level'] == 'MEDIUM']),
            'Low': len(df[df['Risk Level'] == 'LOW']),
            'Cases': df['Case ID'].nunique(),
            'Countries': df['Country'].nunique(),
            'Earliest Date': df['Timestamp'].min(),
            'Latest Date': df['Timestamp'].max()
        })

summary_df = pd.DataFrame(summary)
summary_df.to_csv("case_files/cases_summary.csv", index=False)
print(f"✅ Summary saved to case_files/cases_summary.csv")
print(f"📁 Total files generated: {len(summary)}")

# Display summary
print("\n📈 QUICK SUMMARY:")
print(f"   Total Evidence Records: {summary_df['Total Records'].sum():,}")
print(f"   Total Critical Items: {summary_df['Critical'].sum():,}")
print(f"   Total High Risk Items: {summary_df['High'].sum():,}")
print(f"   Average per case: {summary_df['Total Records'].mean():.0f} records")

print("\n" + "=" * 50)
print("✅ READY TO USE IN YOUR UFDR TOOL!")
print("=" * 50)