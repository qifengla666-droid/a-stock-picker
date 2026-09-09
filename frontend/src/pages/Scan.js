import React, { useState } from 'react';
import {
  Card,
  Form,
  InputNumber,
  Button,
  Table,
  Spin,
  Alert,
  Row,
  Col,
  Space,
  Tag,
} from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import { stockApi } from '../services/api';

function Scan() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [hasScanned, setHasScanned] = useState(false);

  const handleScan = async (values) => {
    try {
      setLoading(true);
      setError(null);
      const response = await stockApi.scanStocks(values);
      setResults(response || []);
      setHasScanned(true);
    } catch (err) {
      setError('选股扫描失败，请检查参数设置');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'code',
      key: 'code',
      width: 100,
      render: (text) => <span style={{ fontWeight: 'bold' }}>{text}</span>,
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
    },
    {
      title: '技术面评分',
      dataIndex: 'technical_score',
      key: 'technical_score',
      width: 120,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '基本面评分',
      dataIndex: 'fundamental_score',
      key: 'fundamental_score',
      width: 120,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '资金面评分',
      dataIndex: 'money_flow_score',
      key: 'money_flow_score',
      width: 120,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '综合评分',
      dataIndex: 'overall_score',
      key: 'overall_score',
      width: 120,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 70 ? 'blue' : 'orange'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <a href={`/analysis/${record.code}`}>分析详情</a>
      ),
    },
  ];

  return (
    <div>
      <h1>选股扫描</h1>

      <Card title="筛选条件" style={{ marginBottom: 24 }}>
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            technical_min_score: 60,
            fundamental_min_score: 60,
            money_flow_min_score: 50,
            overall_min_score: 70,
            limit: 50,
          }}
          onFinish={handleScan}
        >
          <Row gutter={16}>
            <Col xs={24} sm={12} lg={6}>
              <Form.Item
                label="技术面最低分"
                name="technical_min_score"
                tooltip="技术面评分下限（0-100）"
              >
                <InputNumber min={0} max={100} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Form.Item
                label="基本面最低分"
                name="fundamental_min_score"
                tooltip="基本面评分下限（0-100）"
              >
                <InputNumber min={0} max={100} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Form.Item
                label="资金面最低分"
                name="money_flow_min_score"
                tooltip="资金面评分下限（0-100）"
              >
                <InputNumber min={0} max={100} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Form.Item
                label="综合最低分"
                name="overall_min_score"
                tooltip="综合评分下限（0-100）"
              >
                <InputNumber min={0} max={100} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24} sm={12} lg={6}>
              <Form.Item label="返回数量限制" name="limit" tooltip="最多返回多少结果">
                <InputNumber min={1} max={500} />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" icon={<SearchOutlined />} loading={loading}>
                开始扫描
              </Button>
              <Button icon={<ReloadOutlined />} onClick={() => form.resetFields()}>
                重置
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {error && <Alert message={error} type="error" showIcon style={{ marginBottom: 16 }} />}

      {hasScanned && (
        <Card
          title={`扫描结果 (共 ${results.length} 只股票符合条件)`}
          loading={loading}
        >
          <Table
            dataSource={results}
            columns={columns}
            rowKey="code"
            pagination={{ pageSize: 20, showSizeChanger: true }}
            scroll={{ x: 1000 }}
          />
        </Card>
      )}
    </div>
  );
}

export default Scan;
