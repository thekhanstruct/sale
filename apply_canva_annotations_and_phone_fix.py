import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update photos logic in fetchInventory to attach generated clear product photos
old_photos_code = '''let photos = [];
                if (rawImg1) photos.push(rawImg1);
                
                // Merge scraped retailer photos if available
                if (scraped.images && Array.isArray(scraped.images)) {
                    scraped.images.forEach(img => {
                        if (img && !photos.includes(img)) photos.push(img);
                    });
                }

                [13, 15, 16, 17, 18, 19].forEach(colIdx => {
                    let extra = cols[colIdx]?.trim();
                    if (extra && extra !== '#' && !extra.startsWith('http://') && !extra.startsWith('https://')) {
                        if (!extra.startsWith('http') && !extra.startsWith('images/')) {
                            extra = 'images/' + extra;
                        }
                        extra = extra.replace(/\\.(HEIC|HEIF|PNG|png)$/i, '.jpeg');
                        if ((extra.includes('IMG_') || extra.includes('.jpeg') || extra.includes('.jpg')) && !photos.includes(extra)) {
                            photos.push(extra);
                        }
                    }
                });'''

new_photos_code = '''let photos = [];
                if (rawImg1) photos.push(rawImg1);
                
                // Add generated clear studio product photos for specific items
                let nLower = fullName.toLowerCase();
                if (nLower.includes('clear corner shelf') || nLower.includes('clear corner shelves')) {
                    if (!photos.includes('images/clear_corner_shelf_gen.jpg')) photos.push('images/clear_corner_shelf_gen.jpg');
                } else if (nLower.includes('wood grain corner shelf') || nLower.includes('wood grain corner shelves')) {
                    if (!photos.includes('images/wood_grain_corner_shelf_gen.jpg')) photos.push('images/wood_grain_corner_shelf_gen.jpg');
                } else if (nLower.includes('hudson clear') || nLower.includes('storage bin')) {
                    if (!photos.includes('images/clear_storage_bin_gen.jpg')) photos.push('images/clear_storage_bin_gen.jpg');
                }

                // Merge scraped retailer photos if available
                if (scraped.images && Array.isArray(scraped.images)) {
                    scraped.images.forEach(img => {
                        if (img && !photos.includes(img)) photos.push(img);
                    });
                }

                [13, 15, 16, 17, 18, 19].forEach(colIdx => {
                    let extra = cols[colIdx]?.trim();
                    if (extra && extra !== '#' && !extra.startsWith('http://') && !extra.startsWith('https://')) {
                        if (!extra.startsWith('http') && !extra.startsWith('images/')) {
                            extra = 'images/' + extra;
                        }
                        extra = extra.replace(/\\.(HEIC|HEIF|PNG|png)$/i, '.jpeg');
                        if ((extra.includes('IMG_') || extra.includes('.jpeg') || extra.includes('.jpg')) && !photos.includes(extra)) {
                            photos.push(extra);
                        }
                    }
                });'''

content = content.replace(old_photos_code, new_photos_code)

# 2. Update card image wrap: remove red-circled overlays (top-left & top-right), add right vertical thumbnail strip & bottom right next arrow button [ → ]
old_image_wrap_regex = r'<div class="card-image-wrap" id="img-wrap-\$\{item\.id\}"[\s\S]*?</div>\s*</div>'

new_image_wrap = '''<div class="card-image-wrap" id="img-wrap-${item.id}" style="position: relative; width: 100%; height: 260px; overflow: hidden; background-color: #f7f8fa; display: flex; align-items: center;">
                        <!-- Main Product Image -->
                        <div style="flex: 1; height: 100%; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                            <img id="img-${item.id}" src="${activePhoto}" alt="${item.name}" class="item-img" loading="lazy" onclick="openLightbox('${item.id}', itemPhotoState['${item.id}']?.currentIdx || 0, event)" style="width: 100%; height: 100%; object-fit: contain; padding: 8px; display: block; cursor: pointer;" onerror="this.onerror=null; this.src='https://placehold.co/600x600/f0f2f5/65676b?text=Garage+Sale+Item'">

                            ${item.photos.length > 1 ? `
                            <!-- Next Arrow Pill Button on Bottom Right [ → ] -->
                            <button onclick="nextCardImage('${item.id}', event)" title="Next Photo" style="position: absolute; bottom: 10px; right: 10px; height: 28px; padding: 0 10px; border-radius: 14px; background: rgba(255, 255, 255, 0.92); border: 1px solid #e4e6eb; color: #050505; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 4; box-shadow: 0 2px 4px rgba(0,0,0,0.12);">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                            </button>
                            ` : ''}
                        </div>

                        <!-- Vertical Thumbnail Strip on Right Side -->
                        ${item.photos.length > 1 ? `
                        <div class="card-thumbnails-strip" style="width: 54px; height: 100%; padding: 6px; background: #ffffff; border-left: 1px solid #e4e6eb; display: flex; flex-direction: column; gap: 6px; overflow-y: auto; align-items: center; z-index: 3;">
                            ${item.photos.map((pUrl, pIdx) => `
                                <div onclick="setCardImage('${item.id}', ${pIdx}, event)" style="width: 40px; height: 40px; border-radius: 6px; border: 2px solid ${pIdx === (itemPhotoState[item.id].currentIdx || 0) ? '#1877f2' : '#e4e6eb'}; overflow: hidden; cursor: pointer; flex-shrink: 0; background: #f7f8fa;">
                                    <img src="${pUrl}" alt="Thumbnail ${pIdx+1}" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                            `).join('')}
                        </div>
                        ` : ''}
                    </div>'''

content = re.sub(old_image_wrap_regex, new_image_wrap, content, count=1)

# 3. Update Message Seller link to use direct sms:832-382-1675 anchor
old_msg_seller_btn = r'<button class="btn-secondary" onclick="window\.open\(\'sms:8323821675\?body=[\s\S]*?Message Seller\s*</button>'

new_msg_seller_anchor = '''<a href="sms:832-382-1675?body=Hi%2C%20I%20have%20a%20question%20about%20the%20${encodeURIComponent(item.name)}" class="btn-secondary" style="width: 100%; padding: 0.75rem; border-radius: 8px; font-weight: 600; font-size: 0.92rem; cursor: pointer; background-color: #f0f2f5; color: #050505; border: 1px solid #e4e6eb; display: flex; align-items: center; justify-content: center; text-align: center; margin-top: 0.25rem; text-decoration: none; box-sizing: border-box;">
                                Message Seller
                            </a>'''

content = re.sub(old_msg_seller_btn, new_msg_seller_anchor, content, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Canva annotations & phone link update complete!")
