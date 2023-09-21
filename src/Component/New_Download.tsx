import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Image,
  InputGroup,
  FormControl,
} from "react-bootstrap";
import { PlusSquare, Save, Clipboard } from "react-bootstrap-icons";
import fileIcon from "../assets/categoryFile.png";

function New_Download({ url = "", savePath = "", catg = "", size = "10mo" }) {
  return (
    <Container style={{width: "500px", marginTop: "15em", background: "#b1b1b1" }}>
      {/* style={{ width: "fit-content" }} */}
      <div >
        <Row className="pb-3 pt-5 justify-content-center">
          <Form.Group xs={"9"} as={Col} controlId="urlInput">
            <Form.Control size="sm" type="text" placeholder="Enter URL" />
          </Form.Group>
          <Col xs={"auto"}>
            <Clipboard width="fit-content" />
          </Col>
        </Row>
        <Row className="pb-3 justify-content-center">
          <Form.Group xs={"9"} as={Col} controlId="fileOpener">
            <Form.Control size="sm" type="file" accept=".txt" />
          </Form.Group>
          <Col xs={"auto"}>
            <Save />
          </Col>
        </Row>
        <Row className="pb-3 justify-content-center">
          <Form.Group  xs={"9"} as={Col} controlId="categorySelect">
            <Form.Select size="sm">
              <option>Category 1</option>
              <option>Category 2</option>
              <option>Category 3</option>
            </Form.Select>
          </Form.Group>
          <Col xs={"auto"}>
            <PlusSquare />
          </Col>
        </Row>
      </div>
      <Row className="pb-3  justify-content-end align-items-center" >
        <Form.Group xs={"auto"} as={Col} controlId="checkbox">
          <Form.Check
            type="checkbox"
            label="Remember path for this Category "
          />
        </Form.Group>
        <Col xs={"auto"}>
          <Image width="55" src={fileIcon} alt="Image 1" />
          <p>10mo</p>
        </Col>
      </Row>
      <Row className="pb-4 justify-content-end">
        <Col>
          <Button variant="primary">Button 1</Button>
        </Col>
        <Col>
          <Button variant="secondary">Button 2</Button>
        </Col>
        <Col>
          <Button variant="success">Button 3</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default New_Download;
