#!/usr/bin/env python3
"""
Create A3 landscape PDF from class diagram PNG, fitting it across 2 pages vertically
"""

from PIL import Image
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import math
import os

# A3 landscape dimensions in points (1 point = 1/72 inch)
A3_LANDSCAPE = landscape(A3)
PAGE_WIDTH = A3_LANDSCAPE[0]  # 1190.55 points
PAGE_HEIGHT = A3_LANDSCAPE[1]  # 841.89 points

# Margins
MARGIN = 36  # 0.5 inch margins
USABLE_WIDTH = PAGE_WIDTH - (2 * MARGIN)
USABLE_HEIGHT = PAGE_HEIGHT - (2 * MARGIN)

def create_pdf(image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    print(f"Original image size: {img_width}x{img_height}")
    print(f"A3 landscape page size: {PAGE_WIDTH:.2f}x{PAGE_HEIGHT:.2f} points")
    print(f"Usable area per page: {USABLE_WIDTH:.2f}x{USABLE_HEIGHT:.2f} points")
    
    # For 2 vertical pages
    total_usable_height = USABLE_HEIGHT * 2
    
    print(f"Total usable height for 2 pages: {total_usable_height:.2f} points")
    
    # Scale to fit width on one page and height on 2 pages
    scale_width = USABLE_WIDTH / img_width
    scale_height = total_usable_height / img_height
    
    # Use the smaller scale to ensure everything fits
    scale = min(scale_width, scale_height)
    
    # Calculate scaled dimensions
    scaled_width = img_width * scale
    scaled_height = img_height * scale
    
    print(f"Scale factor: {scale:.4f}")
    print(f"Scaled image size: {scaled_width:.2f}x{scaled_height:.2f} points")
    
    # Split the image into 2 parts
    # Top half and bottom half
    split_height = img_height // 2
    
    # Create top and bottom halves
    img_top = img.crop((0, 0, img_width, split_height))
    img_bottom = img.crop((0, split_height, img_width, img_height))
    
    print(f"Top half: {img_top.size}, Bottom half: {img_bottom.size}")
    
    # Save temporary images
    temp_top = "temp_top.png"
    temp_bottom = "temp_bottom.png"
    img_top.save(temp_top, "PNG")
    img_bottom.save(temp_bottom, "PNG")
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=A3_LANDSCAPE)
    
    # Calculate dimensions for each half
    top_scaled_width = img_top.width * scale
    top_scaled_height = img_top.height * scale
    bottom_scaled_width = img_bottom.width * scale
    bottom_scaled_height = img_bottom.height * scale
    
    # Page 1: Top half
    x_pos = MARGIN + (USABLE_WIDTH - top_scaled_width) / 2
    y_pos = MARGIN + (USABLE_HEIGHT - top_scaled_height) / 2
    
    c.drawImage(temp_top, x_pos, y_pos, width=top_scaled_width, height=top_scaled_height, preserveAspectRatio=True)
    c.setFont("Helvetica", 10)
    c.drawString(PAGE_WIDTH - 80, 20, "Page 1 of 2 (Top)")
    
    # Page 2: Bottom half
    c.showPage()
    x_pos = MARGIN + (USABLE_WIDTH - bottom_scaled_width) / 2
    y_pos = MARGIN + (USABLE_HEIGHT - bottom_scaled_height) / 2
    
    c.drawImage(temp_bottom, x_pos, y_pos, width=bottom_scaled_width, height=bottom_scaled_height, preserveAspectRatio=True)
    c.setFont("Helvetica", 10)
    c.drawString(PAGE_WIDTH - 80, 20, "Page 2 of 2 (Bottom)")
    
    c.save()
    print(f"\nPDF created successfully: {output_path}")
    
    # Clean up
    os.remove(temp_top)
    os.remove(temp_bottom)

if __name__ == "__main__":
    create_pdf("class-diagram.png", "class-diagram-a3.pdf")
