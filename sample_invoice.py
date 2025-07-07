from PIL import Image, ImageDraw, ImageFont

def generate_sample_invoice(path="sample_invoice.png"):
    width, height = 800, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Sample Invoice Text
    text_lines = [
        "INVOICE",
        "",
        "Invoice Number: INV-0001",
        "Date: 2025-07-07",
        "",
        "Bill To:",
        "John Doe",
        "123 Example Street",
        "Cityville, Country",
        "",
        "Description            Qty     Unit Price    Total",
        "---------------------------------------------------",
        "Widget A               2       $50.00         $100.00",
        "Service B              1       $150.00        $150.00",
        "",
        "Subtotal:                                 $250.00",
        "Tax (10%):                                $25.00",
        "Total:                                    $275.00"
    ]

    # Optional: use default font (no need to install TTF)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    y = 20
    for line in text_lines:
        draw.text((40, y), line, fill="black", font=font)
        y += 30

    image.save(path)
    print(f"Sample invoice saved to {path}")

# Generate the sample invoice
generate_sample_invoice()
