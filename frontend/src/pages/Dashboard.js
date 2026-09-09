import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Spin, Alert, Button, Space } from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  SearchOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import { stockApi } from '../services/api';

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalStocks: 0,
    lastScanDate: '-',
    scanCount: 0,
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);

      // 获取统计数据
      const stocks = await stockApi.getStocks(0, 1);
      const history = await stockApi.getScanHistory(0, 1);

      setStats({
        totalStocks: stocks.length || 0,
        lastScanDate: history.length > 0 ? history[0].scan_date : '-',
        scanCount: history.length || 0,
      });
    } catch (err) {
      setError('加载数据失败，请检查后端服务是否正常运行');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSyncStocks = async () => {
    try {
      setLoading(true);
      await stockApi.syncStocks();
      setError(null);
      loadDashboard();
    } catch (err) {
      setError('同步股票失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>仪表盘</h1>
      {error && <Alert message={error} type="warning" showIcon style={{ marginBottom: 16 }} />}

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总股票数"
              value={stats.totalStocks}
              prefix={<ArrowUpOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="最后扫描日期"
              value={stats.lastScanDate}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="扫描记录"
              value={stats.scanCount}
              prefix={<ArrowDownOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="系统状态" value="正常" valueStyle={{ color: '#3f8600' }} />
          </Card>
        </Col>
      </Row>

      <Card title="快速操作" style={{ marginBottom: 24 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <p>⚡ 快速开始选股分析</p>
          <Space>
            <Button type="primary" icon={<ReloadOutlined />} onClick={handleSyncStocks} loading={loading}>
              同步股票数据
            </Button>
            <Button type="primary" icon={<SearchOutlined />}>
              开始选股扫描
            </Button>
          </Space>
        </Space>
      </Card>

      <Card title="使用说明">
        <ol>
          <li>点击"同步股票数据"获取最新的A股列表</li>
          <li>在"选股扫描"页面设置筛选条件并执行扫描</li>
          <li>在"分析报告"查看详细的技术面、基本面、资金面分析</li>
          <li>在"历史记录"查看历次扫描的结果</li>
        </ol>
      </Card>
    </div>
  );
}

export default Dashboard;
