import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu, Button, Space } from 'antd';
import {
  DashboardOutlined,
  SearchOutlined,
  AnalysisOutlined,
  HistoryOutlined,
  SettingOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import Dashboard from './pages/Dashboard';
import Scan from './pages/Scan';
import Analysis from './pages/Analysis';
import History from './pages/History';
import './App.css';

const { Header, Sider, Content, Footer } = Layout;

function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKey, setSelectedKey] = useState(['1']);

  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: '仪表盘',
      path: '/',
    },
    {
      key: '2',
      icon: <SearchOutlined />,
      label: '选股扫描',
      path: '/scan',
    },
    {
      key: '3',
      icon: <AnalysisOutlined />,
      label: '分析报告',
      path: '/analysis',
    },
    {
      key: '4',
      icon: <HistoryOutlined />,
      label: '历史记录',
      path: '/history',
    },
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider trigger={null} collapsible collapsed={collapsed} width={200}>
          <div className="logo">
            <h2>📈 选股工具</h2>
          </div>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={selectedKey}
            items={menuItems}
            onClick={(e) => {
              setSelectedKey([e.key]);
              const item = menuItems.find((m) => m.key === e.key);
              if (item) window.location.href = item.path;
            }}
          />
        </Sider>

        <Layout>
          <Header
            style={{
              background: '#fff',
              padding: '0 24px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Button
              type="text"
              icon={collapsed ? '☰' : '✕'}
              onClick={() => setCollapsed(!collapsed)}
              style={{ fontSize: '18px' }}
            />
            <Space>
              <Button type="text" icon={<SettingOutlined />}>
                设置
              </Button>
              <Button type="text" icon={<LogoutOutlined />}>
                退出
              </Button>
            </Space>
          </Header>

          <Content style={{ margin: '24px 16px', padding: '24px', background: '#fff' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/scan" element={<Scan />} />
              <Route path="/analysis/:code" element={<Analysis />} />
              <Route path="/history" element={<History />} />
            </Routes>
          </Content>

          <Footer style={{ textAlign: 'center', background: '#f0f2f5' }}>
            <p>A股选股工具 © 2024 | 综合分析平台 | 仅供学习和研究使用</p>
          </Footer>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;
