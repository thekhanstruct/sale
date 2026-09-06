import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the card rendering template inside container.innerHTML = filtered.map(...)
old_card_template_regex = r'return `\s*<div class="item-card [\s\S]*?</div>\s*</div>\s*`;'

new_card_template = '''// Register photos in itemPhotoState
                if (!itemPhotoState[item.id]) {
                    itemPhotoState[item.id] = { currentIdx: 0, photos: item.photos };
                } else {
                    itemPhotoState[item.id].photos = item.photos;
                }
                const activePhoto = item.photos[itemPhotoState[item.id].currentIdx || 0] || item.rawImg1;

                return `
                <div class="item-card ${isExpanded ? 'expanded' : ''}" style="background-color: #ffffff; border-radius: 12px; border: 1px solid #e4e6eb; overflow: hidden; display: flex; flex-direction: column; animation-delay: ${index * 0.03}s;">
                    <div class="card-image-wrap" id="img-wrap-${item.id}" style="position: relative; width: 100%; height: 260px; overflow: hidden; background-color: #f7f8fa;">
                        ${discountPercent > 0 ? `<div class="card-badge-discount" style="position: absolute; top: 10px; left: 10px; background: #e41e3f; color: #ffffff; font-size: 0.75rem; font-weight: 700; padding: 4px 8px; border-radius: 6px; letter-spacing: 0.5px; z-index: 3; box-shadow: 0 2px 6px rgba(228, 30, 63, 0.3); text-transform: uppercase;">${discountPercent}% OFF</div>` : ''}
                        
                        <div class="card-badges-right" style="position: absolute; top: 10px; right: 10px; display: flex; flex-direction: column; gap: 4px; align-items: flex-end; z-index: 3;">
                            <div class="card-badge-qty" style="background: rgba(255, 255, 255, 0.92); color: #050505; font-size: 0.72rem; font-weight: 600; padding: 3px 8px; border-radius: 6px; border: 1px solid #e4e6eb;">${qtyBadgeText}</div>
                            <div class="condition-badge-top" style="background: rgba(240, 242, 245, 0.92); color: #65676b; font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; border: 1px solid #e4e6eb;">${item.condition}</div>
                        </div>

                        <img id="img-${item.id}" src="${activePhoto}" alt="${item.name}" class="item-img" loading="lazy" onclick="toggleItem('${item.id}')" style="width: 100%; height: 100%; object-fit: contain; padding: 8px; display: block; cursor: pointer;" onerror="this.onerror=null; this.src='https://placehold.co/600x600/f0f2f5/65676b?text=Garage+Sale+Item'">

                        ${item.photos.length > 1 ? `
                            <button class="carousel-arrow left" onclick="prevCardImage('${item.id}', event)" title="Previous photo" style="position: absolute; left: 8px; top: 50%; transform: translateY(-50%); width: 32px; height: 32px; border-radius: 50%; background: rgba(255, 255, 255, 0.92); border: 1px solid #e4e6eb; color: #050505; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 4; box-shadow: 0 2px 4px rgba(0,0,0,0.12);">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
                            </button>
                            <button class="carousel-arrow right" onclick="nextCardImage('${item.id}', event)" title="Next photo" style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); width: 32px; height: 32px; border-radius: 50%; background: rgba(255, 255, 255, 0.92); border: 1px solid #e4e6eb; color: #050505; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 4; box-shadow: 0 2px 4px rgba(0,0,0,0.12);">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </button>

                            <div class="carousel-dots-wrap" style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; align-items: center; background: rgba(0, 0, 0, 0.55); padding: 4px 8px; border-radius: 12px; backdrop-filter: blur(4px); z-index: 4;">
                                ${item.photos.map((_, pIdx) => `<span id="dot-${item.id}-${pIdx}" class="carousel-dot ${pIdx === (itemPhotoState[item.id].currentIdx || 0) ? 'active' : ''}" onclick="setCardImage('${item.id}', ${pIdx}, event)" style="width: ${pIdx === (itemPhotoState[item.id].currentIdx || 0) ? '8px' : '6px'}; height: ${pIdx === (itemPhotoState[item.id].currentIdx || 0) ? '8px' : '6px'}; border-radius: 50%; background: ${pIdx === (itemPhotoState[item.id].currentIdx || 0) ? '#ffffff' : 'rgba(255, 255, 255, 0.45)'}; cursor: pointer; transition: all 0.2s ease;"></span>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="card-content" style="padding: 1.15rem; display: flex; flex-direction: column; gap: 0.65rem; flex: 1;">
                        <div class="card-header" onclick="toggleItem('${item.id}')" style="cursor: pointer;">
                            <span class="item-category" style="font-size: 0.72rem; color: #65676b; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700;">${item.category}</span>
                            <h3 class="item-title" style="font-size: 1.1rem; font-weight: 700; margin: 0.2rem 0; line-height: 1.35; color: #050505;">${item.name}</h3>
                        </div>

                        <div class="card-pricing-block" style="display: flex; justify-content: space-between; align-items: baseline; margin: 0.25rem 0;">
                            <div class="price-main-wrap" style="display: flex; align-items: baseline; gap: 0.5rem;">
                                <span class="price-current" style="font-size: 1.65rem; font-weight: 800; color: #050505; letter-spacing: -0.5px;">$${item.price.toFixed(2)}</span>
                                ${origFormatted ? `<span class="price-original" style="font-size: 1rem; color: #65676b; text-decoration: line-through; font-weight: 500;">${origFormatted}</span>` : ''}
                            </div>
                            ${savingsText ? `<span class="savings-pill" style="background: #ffebe9; border: 1px solid #fcd3d1; color: #d9381e; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; white-space: nowrap;">${savingsText}</span>` : ''}
                        </div>

                        <!-- Action Buttons Row (3 Side-by-Side): [ Save ] [ Buy Now - $X ] [ Expand Details ^ / Hide Details ^ ] -->
                        <div class="card-actions-row" style="display: flex; gap: 0.4rem; margin: 0.25rem 0; width: 100%;">
                            <button class="btn-card-save ${isSaved ? 'saved' : ''}" onclick="toggleSaved('${item.id}', event)" style="flex: 1; min-width: 0; display: flex; align-items: center; justify-content: center; gap: 0.3rem; height: 38px; padding: 0 0.4rem; border-radius: 8px; border: 1px solid ${isSaved ? '#ef4444' : '#e4e6eb'}; background: ${isSaved ? '#ffebe9' : '#ffffff'}; color: ${isSaved ? '#ef4444' : '#050505'}; font-size: 0.78rem; font-weight: 600; cursor: pointer; white-space: nowrap;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="${isSaved ? '#ef4444' : 'none'}" stroke="${isSaved ? '#ef4444' : 'currentColor'}" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                                <span>${isSaved ? 'Saved' : 'Save'}</span>
                            </button>

                            <button class="btn-primary" onclick="openBuyModal('${item.id}')" ${item.status !== 'Available' ? 'disabled' : ''} style="flex: 1.3; min-width: 0; display: flex; align-items: center; justify-content: center; height: 38px; padding: 0 0.4rem; border-radius: 8px; font-weight: 700; font-size: 0.8rem; cursor: pointer; border: none; background-color: #1877f2; color: white; text-align: center; white-space: nowrap;">
                                ${item.status === 'Available' ? `Buy Now - $${item.price.toFixed(2)}` : 'Item Sold'}
                            </button>

                            <button class="btn-card-expand" onclick="toggleItem('${item.id}')" style="flex: 1.1; min-width: 0; display: flex; align-items: center; justify-content: center; gap: 0.25rem; height: 38px; padding: 0 0.4rem; border-radius: 8px; border: 1px solid #e4e6eb; background: #ffffff; color: #050505; font-size: 0.75rem; font-weight: 600; cursor: pointer; white-space: nowrap;">
                                <span>${isExpanded ? 'Hide Details' : 'Expand Details'}</span>
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="${isExpanded ? '18 15 12 9 6 15' : '6 9 12 15 18 9'}"></polyline></svg>
                            </button>
                        </div>

                        ${hasRetailerLink ? `
                        <div class="retailer-compare-row" style="margin: 0.25rem 0;">
                            <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="retailer-compare-btn" title="Compare price at ${item.retailer}" style="display: flex; align-items: center; justify-content: space-between; width: 100%; height: 42px; padding: 0 12px; background: #f7f8fa; border: 1px solid #e4e6eb; border-radius: 8px; text-decoration: none; box-sizing: border-box;">
                                <span class="compare-text" style="font-size: 0.82rem; font-weight: 600; color: #050505;">Compare Price</span>
                                <div class="compare-logo-wrap" style="display: inline-flex; align-items: center; justify-content: center; height: 26px; padding: 2px 10px; background: #ffffff; border: 1px solid #e4e6eb; border-radius: 6px; flex-shrink: 0;">${getRetailerLogoSvg(item.retailer)}</div>
                                <svg class="compare-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#050505" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>
                            </a>
                        </div>` : ''}

                        ${isExpanded ? `
                        <div class="card-expanded-content" style="margin-top: 0.5rem; padding-top: 0.75rem; border-top: 1px solid #e4e6eb; display: flex; flex-direction: column; gap: 0.75rem;">
                            <p class="item-desc" style="font-size: 0.85rem; color: #65676b; line-height: 1.5; margin: 0;">${item.desc}</p>
                            
                            <div class="specs-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                                <div class="spec-box" style="background-color: #f7f8fa; padding: 0.65rem; border-radius: 8px; border: 1px solid #e4e6eb;">
                                    <label style="display: block; font-size: 0.65rem; color: #65676b; margin-bottom: 0.2rem; letter-spacing: 0.5px;">DIMENSIONS</label>
                                    <span style="font-size: 0.82rem; font-weight: 600; color: #050505;">${item.dimensions && item.dimensions !== 'N/A' ? item.dimensions : (item.size && item.size !== 'N/A' ? item.size : 'Standard')}</span>
                                </div>
                                <div class="spec-box" style="background-color: #f7f8fa; padding: 0.65rem; border-radius: 8px; border: 1px solid #e4e6eb;">
                                    <label style="display: block; font-size: 0.65rem; color: #65676b; margin-bottom: 0.2rem; letter-spacing: 0.5px;">CONDITION</label>
                                    <span style="font-size: 0.82rem; font-weight: 600; color: #050505;">${item.condition}</span>
                                </div>
                                <div class="spec-box" style="background-color: #f7f8fa; padding: 0.65rem; border-radius: 8px; border: 1px solid #e4e6eb; display: flex; flex-direction: column; justify-content: center;">
                                    <label style="display: block; font-size: 0.65rem; color: #65676b; margin-bottom: 0.2rem; letter-spacing: 0.5px;">RETAILER</label>
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <span style="font-size: 0.82rem; font-weight: 600; color: #050505;">${item.retailer}</span>
                                        ${getRetailerLogoSvg(item.retailer)}
                                    </div>
                                </div>
                                <div class="spec-box" style="background-color: #f7f8fa; padding: 0.65rem; border-radius: 8px; border: 1px solid #e4e6eb;">
                                    <label style="display: block; font-size: 0.65rem; color: #65676b; margin-bottom: 0.2rem; letter-spacing: 0.5px;">STATUS</label>
                                    <span style="font-size: 0.82rem; font-weight: 600; color: ${item.status === 'Available' ? '#31a24c' : '#e41e3f'}">● ${item.status}</span>
                                </div>
                            </div>
                            
                            <button class="btn-secondary" onclick="window.open('sms:8323821675?body=Hi%2C%20I%20have%20a%20question%20about%20the%20${encodeURIComponent(item.name)}')" style="width: 100%; padding: 0.75rem; border-radius: 8px; font-weight: 600; font-size: 0.92rem; cursor: pointer; background-color: #f0f2f5; color: #050505; border: 1px solid #e4e6eb; display: flex; align-items: center; justify-content: center; text-align: center; margin-top: 0.25rem;">
                                Message Seller
                            </button>
                        </div>
                        ` : ''}
                    </div>
                </div>
                `;'''

content = re.sub(old_card_template_regex, new_card_template, content, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Canva mockup layout script executed!")
