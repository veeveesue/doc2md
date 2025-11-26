// Configuration
const SERVER_URL = 'http://localhost:8765';

// DOM Elements
const fileInput = document.getElementById('fileInput');
const folderInput = document.getElementById('folderInput');
const fileInfo = document.getElementById('fileInfo');
const folderInfo = document.getElementById('folderInfo');
const extractImages = document.getElementById('extractImages');
const autoConvert = document.getElementById('autoConvert');
const outputPath = document.getElementById('outputPath');
const clearOutput = document.getElementById('clearOutput');
const convertBtn = document.getElementById('convertBtn');
const serverStatus = document.getElementById('serverStatus');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const serverUrl = document.getElementById('serverUrl');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const results = document.getElementById('results');

// State
let selectedFiles = [];
let isServerOnline = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  serverUrl.textContent = SERVER_URL;
  checkServerStatus();
  loadSettings();
});

// Event Listeners
fileInput.addEventListener('change', handleFileSelect);
folderInput.addEventListener('change', handleFolderSelect);
clearOutput.addEventListener('click', () => {
  outputPath.value = '';
  saveSettings();
});
convertBtn.addEventListener('click', handleConvert);
extractImages.addEventListener('change', saveSettings);
autoConvert.addEventListener('change', saveSettings);
outputPath.addEventListener('change', saveSettings);

// Check server status
async function checkServerStatus() {
  try {
    const response = await fetch(`${SERVER_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (response.ok) {
      setServerStatus(true, '服务器已连接 ✓');
    } else {
      setServerStatus(false, '服务器响应异常');
    }
  } catch (error) {
    setServerStatus(false, '服务器未运行 - 请先启动服务器');
  }
}

function setServerStatus(online, message) {
  isServerOnline = online;
  statusText.textContent = message;

  if (online) {
    statusIndicator.textContent = '🟢';
    serverStatus.classList.add('connected');
    serverStatus.classList.remove('disconnected');
  } else {
    statusIndicator.textContent = '🔴';
    serverStatus.classList.add('disconnected');
    serverStatus.classList.remove('connected');
  }

  updateConvertButton();
}

// Handle file selection
function handleFileSelect(e) {
  const files = Array.from(e.target.files);
  selectedFiles = files;

  if (files.length > 0) {
    const fileNames = files.map(f => f.name).join(', ');
    fileInfo.textContent = `已选择 ${files.length} 个文件: ${fileNames}`;
    fileInfo.classList.add('has-files');
    folderInfo.textContent = '未选择文件夹';
    folderInfo.classList.remove('has-files');
  } else {
    fileInfo.textContent = '未选择文件';
    fileInfo.classList.remove('has-files');
  }

  updateConvertButton();
}

// Handle folder selection
function handleFolderSelect(e) {
  const files = Array.from(e.target.files).filter(f =>
    f.name.endsWith('.docx') || f.name.endsWith('.doc')
  );
  selectedFiles = files;

  if (files.length > 0) {
    folderInfo.textContent = `已选择文件夹，找到 ${files.length} 个 Word 文档`;
    folderInfo.classList.add('has-files');
    fileInfo.textContent = '未选择文件';
    fileInfo.classList.remove('has-files');
  } else {
    folderInfo.textContent = '文件夹中未找到 Word 文档';
    folderInfo.classList.remove('has-files');
  }

  updateConvertButton();
}

// Update convert button state
function updateConvertButton() {
  const canConvert = isServerOnline && selectedFiles.length > 0;
  convertBtn.disabled = !canConvert;
}

// Handle conversion
async function handleConvert() {
  if (!isServerOnline || selectedFiles.length === 0) return;

  // Reset UI
  progressSection.style.display = 'block';
  resultsSection.style.display = 'block';
  results.innerHTML = '';
  convertBtn.disabled = true;
  convertBtn.classList.add('converting');
  convertBtn.querySelector('.button-text').textContent = '转换中...';

  const total = selectedFiles.length;
  let completed = 0;
  let succeeded = 0;
  let failed = 0;

  // Process files
  for (const file of selectedFiles) {
    try {
      const result = await convertFile(file);

      if (result.success) {
        succeeded++;
        addResult(true, `✓ ${file.name} → ${result.output_file}`);
      } else {
        failed++;
        addResult(false, `✗ ${file.name}: ${result.error}`);
      }
    } catch (error) {
      failed++;
      addResult(false, `✗ ${file.name}: ${error.message}`);
    }

    completed++;
    updateProgress(completed, total);
  }

  // Update final status
  convertBtn.disabled = false;
  if (failed === 0) {
    convertBtn.classList.remove('converting');
    convertBtn.classList.add('success');
    convertBtn.querySelector('.button-text').textContent = `转换完成 (${succeeded}/${total})`;
    setTimeout(() => {
      convertBtn.classList.remove('success');
      convertBtn.querySelector('.button-text').textContent = '开始转换';
    }, 3000);
  } else {
    convertBtn.classList.remove('converting');
    convertBtn.classList.add('error');
    convertBtn.querySelector('.button-text').textContent = `完成 - ${failed} 个失败`;
    setTimeout(() => {
      convertBtn.classList.remove('error');
      convertBtn.querySelector('.button-text').textContent = '开始转换';
    }, 3000);
  }
}

// Convert single file
async function convertFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('extract_images', extractImages.checked);
  formData.append('auto_convert', autoConvert.checked);

  if (outputPath.value.trim()) {
    formData.append('output_path', outputPath.value.trim());
  }

  const response = await fetch(`${SERVER_URL}/convert`, {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  return result;
}

// Update progress
function updateProgress(current, total) {
  const percentage = (current / total) * 100;
  progressFill.style.width = `${percentage}%`;
  progressText.textContent = `${current} / ${total}`;
}

// Add result item
function addResult(success, message) {
  const item = document.createElement('div');
  item.className = `result-item ${success ? 'success' : 'error'}`;
  item.innerHTML = `
    <span class="icon">${success ? '✓' : '✗'}</span>
    <span class="text">${escapeHtml(message)}</span>
  `;
  results.appendChild(item);
  results.scrollTop = results.scrollHeight;
}

// Escape HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Save settings
function saveSettings() {
  const settings = {
    extractImages: extractImages.checked,
    autoConvert: autoConvert.checked,
    outputPath: outputPath.value
  };
  chrome.storage.local.set({ settings });
}

// Load settings
function loadSettings() {
  chrome.storage.local.get(['settings'], (result) => {
    if (result.settings) {
      extractImages.checked = result.settings.extractImages !== false;
      autoConvert.checked = result.settings.autoConvert || false;
      outputPath.value = result.settings.outputPath || '';
    }
  });
}

// Periodic server check
setInterval(checkServerStatus, 10000);
