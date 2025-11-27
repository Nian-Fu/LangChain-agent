// 配置
const API_BASE_URL = 'http://localhost:8000';
let currentUserId = 'user_' + Math.random().toString(36).substr(2, 9);
let chatHistory = [];

// DOM 加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

// 初始化应用
function initApp() {
    // 标签页切换
    setupTabNavigation();
    
    // 聊天功能
    setupChat();
    
    // 表单提交
    setupForms();
    
    // 检查API状态
    checkAPIStatus();
}

// 设置标签页导航
function setupTabNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-content');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = link.dataset.tab;
            
            // 更新导航状态
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // 切换标签页
            tabContents.forEach(tab => tab.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
}

// 设置聊天功能
function setupChat() {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const newChatBtn = document.getElementById('new-chat-btn');
    const quickBtns = document.querySelectorAll('.quick-btn');
    
    // 发送消息
    sendBtn.addEventListener('click', () => sendMessage());
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // 快捷按钮
    quickBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.dataset.query;
            chatInput.value = query;
            sendMessage();
        });
    });
    
    // 新对话
    newChatBtn.addEventListener('click', () => {
        clearChat();
    });
}

// 发送消息
async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const query = chatInput.value.trim();
    
    if (!query) return;
    
    // 显示用户消息
    addMessageToChat('user', query);
    chatInput.value = '';
    
    // 隐藏欢迎消息，显示聊天区域
    document.getElementById('welcome-message').style.display = 'none';
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.classList.add('active');
    
    // 显示加载状态
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/travel/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                user_id: currentUserId
            })
        });
        
        if (!response.ok) {
            throw new Error('API请求失败');
        }
        
        const data = await response.json();
        
        // 显示助手回复
        addMessageToChat('assistant', data.final_answer || '抱歉，我无法处理您的请求。');
        
        // 显示结构化数据（航班、酒店等）
        if (data.results) {
            displayStructuredResults(data.results, data.intent_type);
        }
        
        // 添加到历史记录
        addToChatHistory(query);
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('assistant', '抱歉，服务暂时不可用。请确保后端服务已启动，并检查API地址配置。');
    } finally {
        hideLoading();
    }
}

// 显示结构化结果（航班、酒店等）
function displayStructuredResults(results, intentType) {
    const chatMessages = document.getElementById('chat-messages');
    
    // 机票结果
    if (results.flight && results.flight.success && results.flight.data) {
        const flights = results.flight.data.flights || [];
        if (flights.length > 0) {
            const flightCards = createFlightCards(flights.slice(0, 3)); // 只显示前3个
            chatMessages.appendChild(flightCards);
        }
    }
    
    // 酒店结果
    if (results.hotel && results.hotel.success && results.hotel.data) {
        const hotels = results.hotel.data.hotels || [];
        if (hotels.length > 0) {
            const hotelCards = createHotelCards(hotels.slice(0, 3)); // 只显示前3个
            chatMessages.appendChild(hotelCards);
        }
    }
    
    // 景点结果
    if (results.attraction && results.attraction.success && results.attraction.data) {
        const attractions = results.attraction.data.attractions || [];
        if (attractions.length > 0) {
            const attractionCards = createAttractionCards(attractions.slice(0, 3));
            chatMessages.appendChild(attractionCards);
        }
    }
    
    // 行程结果
    if (results.itinerary && results.itinerary.success && results.itinerary.data) {
        const itinerary = results.itinerary.data;
        const itineraryCard = createItineraryCard(itinerary);
        chatMessages.appendChild(itineraryCard);
    }
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 创建航班卡片
function createFlightCards(flights) {
    const container = document.createElement('div');
    container.className = 'structured-results';
    container.style.cssText = 'margin: 1rem 0; padding: 1rem; background: var(--background); border-radius: 12px;';
    
    container.innerHTML = '<h4 style="margin-bottom: 1rem; color: var(--primary-color);"><i class="fas fa-plane"></i> 为您找到以下航班</h4>';
    
    flights.forEach(flight => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.cssText = 'margin-bottom: 0.5rem; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="font-weight: 600;">${escapeHtml(flight.airline)} ${escapeHtml(flight.flight_number)}</div>
                <div style="font-size: 1.25rem; color: var(--primary-color); font-weight: 700;">¥${flight.price}</div>
            </div>
            <div style="color: var(--text-light); font-size: 0.9rem;">
                <div style="margin: 0.25rem 0;"><i class="fas fa-clock"></i> ${formatDateTime(flight.departure_time)} - ${formatDateTime(flight.arrival_time)}</div>
                <div style="margin: 0.25rem 0;"><i class="fas fa-hourglass-half"></i> ${escapeHtml(flight.duration)} | <i class="fas fa-route"></i> ${flight.stops === 0 ? '直飞' : flight.stops + '次经停'}</div>
                <div style="margin: 0.25rem 0;"><i class="fas fa-chair"></i> ${flight.cabin_class} | 余票 ${flight.available_seats} 张</div>
            </div>
        `;
        container.appendChild(card);
    });
    
    return container;
}

// 创建酒店卡片
function createHotelCards(hotels) {
    const container = document.createElement('div');
    container.className = 'structured-results';
    container.style.cssText = 'margin: 1rem 0; padding: 1rem; background: var(--background); border-radius: 12px;';
    
    container.innerHTML = '<h4 style="margin-bottom: 1rem; color: var(--primary-color);"><i class="fas fa-hotel"></i> 为您推荐以下酒店</h4>';
    
    hotels.forEach(hotel => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.cssText = 'margin-bottom: 0.5rem; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="font-weight: 600;">${escapeHtml(hotel.name)}</div>
                <div style="font-size: 1.25rem; color: var(--primary-color); font-weight: 700;">¥${hotel.price_per_night}/晚</div>
            </div>
            <div style="color: var(--text-light); font-size: 0.9rem;">
                <div style="margin: 0.25rem 0;"><i class="fas fa-star"></i> ${hotel.star_rating} | 评分 ${hotel.rating} (${hotel.reviews_count}条评价)</div>
                <div style="margin: 0.25rem 0;"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(hotel.address)} | 距市中心 ${hotel.distance_to_center}km</div>
                <div style="margin: 0.25rem 0;"><i class="fas fa-concierge-bell"></i> ${hotel.facilities.slice(0, 3).join(', ')}</div>
            </div>
        `;
        container.appendChild(card);
    });
    
    return container;
}

// 创建景点卡片
function createAttractionCards(attractions) {
    const container = document.createElement('div');
    container.className = 'structured-results';
    container.style.cssText = 'margin: 1rem 0; padding: 1rem; background: var(--background); border-radius: 12px;';
    
    container.innerHTML = '<h4 style="margin-bottom: 1rem; color: var(--primary-color);"><i class="fas fa-landmark"></i> 为您推荐以下景点</h4>';
    
    attractions.forEach(attraction => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.cssText = 'margin-bottom: 0.5rem; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="font-weight: 600;">${escapeHtml(attraction.name)}</div>
                <div style="font-size: 1.1rem; color: var(--primary-color); font-weight: 700;">¥${attraction.ticket_price}</div>
            </div>
            <div style="color: var(--text-light); font-size: 0.9rem;">
                <div style="margin: 0.25rem 0;"><i class="fas fa-star"></i> 评分 ${attraction.rating} | ${escapeHtml(attraction.category)}</div>
                <div style="margin: 0.25rem 0;"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(attraction.address)}</div>
                <div style="margin: 0.25rem 0;">${escapeHtml(attraction.description.substring(0, 80))}...</div>
            </div>
        `;
        container.appendChild(card);
    });
    
    return container;
}

// 创建行程卡片
function createItineraryCard(itinerary) {
    const container = document.createElement('div');
    container.className = 'structured-results';
    container.style.cssText = 'margin: 1rem 0; padding: 1rem; background: var(--background); border-radius: 12px;';
    
    container.innerHTML = `
        <h4 style="margin-bottom: 1rem; color: var(--primary-color);"><i class="fas fa-calendar-alt"></i> ${escapeHtml(itinerary.title)}</h4>
        <div style="padding: 1rem; background: white; border-radius: 8px; margin-bottom: 1rem;">
            <div style="color: var(--text-light); font-size: 0.9rem;">
                <div><i class="fas fa-map-marked-alt"></i> 目的地: ${escapeHtml(itinerary.destination)}</div>
                <div><i class="fas fa-clock"></i> 行程天数: ${itinerary.duration_days}天</div>
                <div><i class="fas fa-dollar-sign"></i> 总费用: ¥${itinerary.total_cost}</div>
            </div>
        </div>
        <div style="font-size: 0.9rem; color: var(--text-light);">点击"行程规划"查看完整行程安排</div>
    `;
    
    return container;
}

// 添加消息到聊天界面
function addMessageToChat(role, content) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">${escapeHtml(content)}</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">${formatMessage(content)}</div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 格式化消息
function formatMessage(text) {
    // 转义HTML
    text = escapeHtml(text);
    // 转换换行符
    text = text.replace(/\n/g, '<br>');
    return text;
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 添加到历史记录
function addToChatHistory(query) {
    chatHistory.push({
        query: query,
        timestamp: new Date()
    });
    
    const historyDiv = document.getElementById('chat-history');
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.style.cssText = 'padding: 0.5rem; margin-bottom: 0.5rem; background: var(--background); border-radius: 8px; cursor: pointer; font-size: 0.9rem;';
    historyItem.textContent = query.substring(0, 30) + (query.length > 30 ? '...' : '');
    historyItem.onclick = () => {
        document.getElementById('chat-input').value = query;
    };
    
    historyDiv.appendChild(historyItem);
}

// 清空聊天
function clearChat() {
    document.getElementById('chat-messages').innerHTML = '';
    document.getElementById('welcome-message').style.display = 'block';
    document.getElementById('chat-messages').classList.remove('active');
}

// 设置表单
function setupForms() {
    // 机票查询表单
    document.getElementById('flight-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleFlightSearch();
    });
    
    // 酒店查询表单
    document.getElementById('hotel-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleHotelSearch();
    });
    
    // 景点推荐表单
    document.getElementById('attraction-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleAttractionSearch();
    });
}

// 处理机票查询
async function handleFlightSearch() {
    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;
    const departureDate = document.getElementById('departure-date').value;
    const passengers = document.getElementById('passengers').value;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/travel/flight`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                departure,
                destination,
                departure_date: departureDate,
                passengers: parseInt(passengers)
            })
        });
        
        const data = await response.json();
        displayFlightResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('机票查询失败，请稍后重试。');
    } finally {
        hideLoading();
    }
}

// 显示机票结果
function displayFlightResults(data) {
    const resultsDiv = document.getElementById('flight-results');
    resultsDiv.innerHTML = '';
    
    if (!data.success) {
        resultsDiv.innerHTML = '<p style="text-align: center; color: var(--danger-color);">查询失败，请重试。</p>';
        return;
    }
    
    const flights = data.data.flights || [];
    
    if (flights.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align: center;">未找到符合条件的航班。</p>';
        return;
    }
    
    // 显示建议
    if (data.suggestion) {
        resultsDiv.innerHTML += `
            <div class="suggestion-box">
                <h4><i class="fas fa-lightbulb"></i> 智能建议</h4>
                <p>${escapeHtml(data.suggestion)}</p>
            </div>
        `;
    }
    
    // 显示航班列表
    flights.forEach(flight => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-header">
                <div class="result-title">
                    <i class="fas fa-plane"></i> ${escapeHtml(flight.airline)} ${escapeHtml(flight.flight_number)}
                </div>
                <div class="result-price">¥${flight.price}</div>
            </div>
            <div class="result-details">
                <div class="result-detail">
                    <i class="fas fa-clock"></i>
                    <span>${formatDateTime(flight.departure_time)} - ${formatDateTime(flight.arrival_time)}</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-hourglass-half"></i>
                    <span>${escapeHtml(flight.duration)}</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-chair"></i>
                    <span>余票 ${flight.available_seats} 张</span>
                </div>
            </div>
            <div class="result-detail" style="margin-top: 0.5rem;">
                <i class="fas fa-route"></i>
                <span>${flight.stops === 0 ? '直飞' : flight.stops + '次经停'}</span>
            </div>
        `;
        resultsDiv.appendChild(card);
    });
}

// 处理酒店查询
async function handleHotelSearch() {
    const destination = document.getElementById('hotel-destination').value;
    const budget = document.getElementById('budget').value;
    const preferences = Array.from(document.querySelectorAll('#hotel-form input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/travel/hotel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                destination,
                budget: budget ? parseFloat(budget) : null,
                preferences
            })
        });
        
        const data = await response.json();
        displayHotelResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('酒店查询失败，请稍后重试。');
    } finally {
        hideLoading();
    }
}

// 显示酒店结果
function displayHotelResults(data) {
    const resultsDiv = document.getElementById('hotel-results');
    resultsDiv.innerHTML = '';
    
    if (!data.success) {
        resultsDiv.innerHTML = '<p style="text-align: center; color: var(--danger-color);">查询失败，请重试。</p>';
        return;
    }
    
    const hotels = data.data.hotels || [];
    
    if (hotels.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align: center;">未找到符合条件的酒店。</p>';
        return;
    }
    
    // 显示建议
    if (data.suggestion) {
        resultsDiv.innerHTML += `
            <div class="suggestion-box">
                <h4><i class="fas fa-lightbulb"></i> 智能建议</h4>
                <p>${escapeHtml(data.suggestion)}</p>
            </div>
        `;
    }
    
    // 显示酒店列表
    hotels.forEach(hotel => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-header">
                <div class="result-title">
                    <i class="fas fa-hotel"></i> ${escapeHtml(hotel.name)}
                </div>
                <div class="result-price">¥${hotel.price_per_night}/晚</div>
            </div>
            <div class="result-details">
                <div class="result-detail">
                    <i class="fas fa-star"></i>
                    <span>${hotel.star_rating} | 评分 ${hotel.rating}</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>距市中心 ${hotel.distance_to_center}km</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-bed"></i>
                    <span>可用 ${hotel.available_rooms} 间</span>
                </div>
            </div>
            <div class="result-detail" style="margin-top: 0.5rem;">
                <i class="fas fa-concierge-bell"></i>
                <span>${hotel.facilities.slice(0, 3).join(', ')}</span>
            </div>
        `;
        resultsDiv.appendChild(card);
    });
}

// 处理景点推荐
async function handleAttractionSearch() {
    const destination = document.getElementById('attraction-destination').value;
    const days = document.getElementById('days').value;
    const preferences = Array.from(document.querySelectorAll('#attraction-form input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/travel/attraction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                destination,
                days: parseInt(days),
                preferences
            })
        });
        
        const data = await response.json();
        displayAttractionResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('景点推荐失败，请稍后重试。');
    } finally {
        hideLoading();
    }
}

// 显示景点结果
function displayAttractionResults(data) {
    const resultsDiv = document.getElementById('attraction-results');
    resultsDiv.innerHTML = '';
    
    if (!data.success) {
        resultsDiv.innerHTML = '<p style="text-align: center; color: var(--danger-color);">推荐失败，请重试。</p>';
        return;
    }
    
    const attractions = data.data.attractions || [];
    
    if (attractions.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align: center;">未找到符合条件的景点。</p>';
        return;
    }
    
    // 显示推荐理由
    if (data.data.recommendation_reason) {
        resultsDiv.innerHTML += `
            <div class="suggestion-box">
                <h4><i class="fas fa-lightbulb"></i> 推荐理由</h4>
                <p>${escapeHtml(data.data.recommendation_reason)}</p>
            </div>
        `;
    }
    
    // 显示景点列表
    attractions.forEach(attraction => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-header">
                <div class="result-title">
                    <i class="fas fa-map-marked-alt"></i> ${escapeHtml(attraction.name)}
                </div>
                <div class="result-price">¥${attraction.ticket_price}</div>
            </div>
            <div class="result-details">
                <div class="result-detail">
                    <i class="fas fa-tag"></i>
                    <span>${escapeHtml(attraction.category)}</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-star"></i>
                    <span>评分 ${attraction.rating}</span>
                </div>
                <div class="result-detail">
                    <i class="fas fa-clock"></i>
                    <span>${escapeHtml(attraction.visit_duration)}</span>
                </div>
            </div>
            <div class="result-detail" style="margin-top: 0.5rem;">
                <i class="fas fa-info-circle"></i>
                <span>${escapeHtml(attraction.opening_hours)}</span>
            </div>
        `;
        resultsDiv.appendChild(card);
    });
}

// 格式化日期时间
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

// 检查API状态
async function checkAPIStatus() {
    const statusDiv = document.getElementById('api-status');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusDiv.className = 'api-status online';
            statusDiv.innerHTML = '<i class="fas fa-check-circle"></i> API服务正常运行';
        } else {
            statusDiv.className = 'api-status offline';
            statusDiv.innerHTML = '<i class="fas fa-times-circle"></i> API服务异常';
        }
    } catch (error) {
        statusDiv.className = 'api-status offline';
        statusDiv.innerHTML = '<i class="fas fa-times-circle"></i> API服务未连接';
    }
}

// 显示加载状态
function showLoading() {
    document.getElementById('loading').classList.add('show');
}

// 隐藏加载状态
function hideLoading() {
    document.getElementById('loading').classList.remove('show');
}

// 显示错误
function showError(message) {
    alert(message);
}

